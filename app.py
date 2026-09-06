from flask import Flask, jsonify, request
from waitress import serve

app = Flask(__name__)

# Formats JSON output with indents and newlines
app.json.compact = False

# In-memory database
events = {}
current_id = 1

@app.route('/items', methods=['GET'])
def get_events():
    # Returns a formatted JSON list of all event objects
    return jsonify(list(events.values())), 200

@app.route('/items/<string:item_id>', methods=['GET'])
def get_event(item_id):
    event = events.get(item_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event), 200

@app.route('/items', methods=['POST'])
def create_event():
    global current_id
    data = request.get_json() or {}
    
    if 'name' not in data or 'location' not in data:
        return jsonify({"error": "Missing required fields: 'name' and 'location'"}), 400

    event_key = f"event{current_id}"
    event = {
        "id": event_key,
        "name": data["name"],
        "status": data.get("status", "open"),
        "location": data["location"],
        "date": data['date']
    }
    events[event_key] = event
    current_id += 1
    
    return jsonify(event), 201

# FIXED: Changed <int:item_id> to <string:item_id>
@app.route('/items/<string:item_id>', methods=['PUT'])
def update_event(item_id):
    if item_id not in events:
        return jsonify({"error": "Event not found"}), 404
    
    data = request.get_json() or {}
    event = events[item_id]
    
    event["name"] = data.get("name", event["name"])
    event["status"] = data.get("status", event["status"])
    event["location"] = data.get("location", event["location"])
    event["date"] = data.get("date", event["date"])
    
    
    return jsonify(event), 200

# FIXED: Changed <int:item_id> to <string:item_id>
@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_event(item_id):
    if item_id not in events:
        return jsonify({"error": "Event not found"}), 404
    
    del events[item_id]
    return jsonify({"message": f"{item_id} deleted"}), 200

if __name__ == '__main__':
    # Production WSGI server listening on port 5000 inside the container
    serve(app, host='0.0.0.0', port=5000)