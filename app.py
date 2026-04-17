from flask import Flask, jsonify, request
app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Task 1: Welcome route (Required by Rubric)
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Event API"}), 200

# GET route (Required by Rubric)
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Task 2: Design and Develop the Code
    data = request.get_json()
    
    # Task 3: Implement validation logic
    if not data or 'title' not in data:
        return jsonify({"error": "Bad Request: Missing title"}), 400
    
    # Task 4: Return and Handle Results
    new_id = events[-1].id + 1 if events else 1
    new_event = Event(new_id, data['title'])
    events.append(new_event)
    
    # Return 201 Created as per Rubric
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Task 2: Design and Develop the Code
    data = request.get_json()
    
    # Task 3: Implement the Loop to find the element
    event = next((e for e in events if e.id == event_id), None)
    
    # Task 4: Return and Handle Results
    if event:
        if 'title' in data:
            event.title = data['title']
            return jsonify(event.to_dict()), 200
        return jsonify({"error": "No title provided"}), 400
    
    return jsonify({"error": "Event not found"}), 404

# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Task 2 & 3: Find the element
    event = next((e for e in events if e.id == event_id), None)
    
    # Task 4: Handle results
    if event:
        events.remove(event)
        return jsonify({"message": "Event deleted successfully"}), 200
    
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)