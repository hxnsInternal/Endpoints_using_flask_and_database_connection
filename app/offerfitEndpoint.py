import datetime
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import database

#Loading enviroment paramters
load_dotenv()
EVENT_TABLE = str(os.getenv('DB_SCHEMA')) + "." + str(os.getenv('EVENT_TABLE'))

print(f"table -> {EVENT_TABLE}")

app = Flask(__name__)
data_store = []  # Store events in memory (could be replaced by a database or .Json File)

# Endpoint to receive and persist JSON events
@app.route('/events', methods=['POST'])
def receive_events():
    try:
        json_data = request.get_json()
        print("entered here")
        # Validate that the JSON has the required keys
        required_keys = ['customer_id', 'event_type', 'timestamp', 'email_id']
        if not all(key in json_data for key in required_keys):
            return jsonify({"status": "error", "message": "Missing required keys"}), 400

        print(f"data type?: {type(json_data)}")
        data_store.append(json_data)

        # Optional: With enough time, we can store information in a database in a better way, for now this part is inserting records in the PostgresDB
        conn = database.get_connection()
        inserted, msg = database.insert_record(EVENT_TABLE, json_data, conn)

        if inserted:
            return jsonify({"status": "success", "message": "Event received and persisted"}), 200
        else:
            return jsonify({"error": msg}), 409

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to retrieve email events for a provided customer_id
@app.route('/events/<customer_id>', methods=['GET'])
def get_events_by_customer_id(customer_id):
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        filtered_events = filter_events(customer_id, start_date, end_date)
        return jsonify({"events": filtered_events}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def filter_events(customer_id, start_date, end_date):
    filtered_events = [event for event in data_store if event.get('customer_id') == int(customer_id)]

    #Applying time range filtering
    if start_date is not None and end_date is not None:
        filtered_events = [event for event in filtered_events if start_date <= event.get('timestamp') <= end_date]

    return filtered_events

def parse_time(time_str):
    # Casting string to timestamp
    return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

@app.route('/drop_events', methods=['POST'])
def drop_events():
    try:
        print("entered to delete all events")
        data_store.clear()

        # Truncate Database table
        conn = database.get_connection()
        database.truncate_table(EVENT_TABLE, conn)

        return jsonify({"status": "success", "message": "All events were deleted"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Minimal testing
def test_receive_events():
    test_app = app.test_client()
    response = test_app.post('/events', json={"customer_id": "789", "event_type": "email_open", "timestamp": "2022-01-01T12:00:00.000Z"})
    assert response.status_code == 200

def test_get_events_by_customer_id():
    test_app = app.test_client()
    response = test_app.get('/events/789')
    assert response.status_code == 200    


if __name__ == '__main__':
    app.run(debug=True)
