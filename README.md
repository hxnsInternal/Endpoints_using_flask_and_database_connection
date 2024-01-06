# endpoints_using_flask_and_database_connection
Here's a small practice using Python, Flask, and PostgreSQL, creating a small API.



/***** Important to read *****/

Use PostgresSQL as the database engine since it is an open-source tool, robust, comprehensive, and with 
many features that facilitate working with data.

The version used was:
	- PostgreSQL 16.1, compiled by Visual C++ build 1937, 64-bit
	- Link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
	
I used Flask as a framework for developing the endpoins

	- https://flask.palletsprojects.com/en/3.0.x/
	
	
/**************************************************************************************************/
Flow of opening and reading the files created to solve the test planned by Offerfit:	

Prerequisites:

1. Install the PostgreSQL version mentioned at the beginning.
2. Open and execute in PgAdmin4 the code present in the file: "02 - PostgreSQL_DDL_querys.sql" to create the necessary database, schemas, and tables for the implementation.

3. Dependency installation:
   - Using the terminal, use the following commands:
     - `pip install Flask`
     - `pip install python-dotenv`
     - `pip install psycopg2-binary`

4. Once the dependencies installation is complete, extract the Python files from the "03 - python_scripts.rar" folder. Within this folder, there are two additional folders, "app" (which contains the files:
   - `.env` -> containing the application's environment variables
   - `database.py` -> containing the connection logic and SQL operations for the PostgreSQL database
   - `offerfitEndpoint.py` -> which contains the logic of the created endpoint to address the requirement

5. Open a terminal and navigate to the path where the "database.py" file is located and execute it using the following command:
   - `python .\offerfitEndpoint.py`

   Once executed, our server will be up and ready to receive requests.

6. In the files and folders contained in the "03 - python_scripts.rar" file, there is a folder called "testing_request," which individually contains different requests to test the functionality of the endpoint:
   - `SendEvents.py`
   - `getEventsByCustomerId.py`
   - `getEventsByCustomerIdTimeFilter.py`
   - `DropAllEvents.py`
   
   You can use these scripts to test the requests.

7. I have attached the JSON file named "04 - offerfit.postman_collection.json" with collections ready to be imported into Postman.
8. Finally, I am attaching the file "05 - Evidences.pdf," which shows screenshots of the correct functioning of the endpoint in both Visual Studio and PostgreSQL.



Thank you for your time, and I hope to have correctly addressed all the requirements. 
I look forward to the opportunity to continue in the process and be part of this great company.

Regards :)
















