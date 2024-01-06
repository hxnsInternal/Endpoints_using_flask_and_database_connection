import json
import os
from dotenv import load_dotenv
import psycopg2
from io import BytesIO


# Loading variables from file .env
load_dotenv()


dbParamenters = {
                    "host": os.getenv('HOST'),
                    "port": os.getenv('PORT'),
                    "database": os.getenv('DATABASE'),
                    "user": os.getenv('USER'),
                    "password": os.getenv('PASSWORD')
                }


#get connection
def get_connection():

    try:
        conn = psycopg2.connect(dbname = dbParamenters['database']
                                ,user = dbParamenters['user']
                                ,password = dbParamenters['password']
                                ,host = dbParamenters['host']
                                ,port = dbParamenters['port'])
        conn.autocommit = True
        print("conectado")
    except Exception as e:
        print(str(e))
        conn.rollback()
        raise e
    else:
        return conn
    

#close connection
def close_connection(connection):

    try:
        connection.close()
        print("cerro conexion")
    except Exception as e:
        print(str(e))
        raise e


#truncate table
def truncate_table(lsTableName, connection):
    try:

        cur = connection.cursor()
        cur.execute(f"TRUNCATE TABLE {lsTableName};")
        print(f"ok truncate --> {lsTableName}")
        connection.commit()
    except Exception as e:
        print(str(e))
        raise e    
    
#insert table If we need to bulk information we can Use this method to transform and insert a Dataframe into a SQL table
def insert_table(table_name, data_frame, fields, conn, add_index=False):
    try:
        output = BytesIO()
        data_frame[fields].to_csv(output, sep='|', header=True, index=add_index)
        output.seek(0)
        copy_query = f"COPY {table_name} ({', '.join(fields)}) FROM STDIN csv DELIMITER '|' NULL '' ESCAPE '\\' HEADER"
        conn.cursor().copy_expert(copy_query, output)
        conn.commit()
        print(f"ok insert table -> {table_name}")
        conn.cursor().close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        return False
    else:
        return True
    

#Insert record in json table
def insert_record(table_name, data, conn):

    msg = ""
    try:
        cursor = conn.cursor()
        json_data = json.dumps(data, ensure_ascii=False)

        # Verify if record already exists
        query = f"SELECT 1 FROM {table_name} WHERE \"event\" = '{json_data}'"    

        cursor.execute(query)

        if cursor.fetchone():
            msg = "Record already exist."
            return False, msg

        # Insert record into table

        insert_query = f"INSERT INTO {table_name} (event) VALUES (%s)"
        
        print(f"sql insert --> {insert_query}")

        cursor.execute(insert_query, [json_data])
        conn.commit()
        msg = "Record inserted successfully."
        cursor.close()
        return True, msg

    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        return False, str(error)

#delete record
def delete_record(table_name, condition_fields, conn):
    msg = ""
    try:
        cursor = conn.cursor()
        # Construir la condición WHERE
        conditions = []
        values = []        

        for key, value in condition_fields.items():
            conditions.append(f"{key} = %s")
            values.append(value)
        
        # Eliminar el registro de la tabla        
        exist_query = f"SELECT 1 FROM {table_name} WHERE {' AND '.join(conditions)}"
        cursor.execute(exist_query, tuple(values))

        if not cursor.fetchone():
            msg = "Record doesn't exist."
            return False, msg   
        
        delete_query = f"DELETE FROM {table_name} WHERE {' AND '.join(conditions)}"
 
        cursor.execute(delete_query, tuple(values))
        conn.commit()
        msg = "Record deleted successfully."
        cursor.close()
        return True, msg
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        return False
