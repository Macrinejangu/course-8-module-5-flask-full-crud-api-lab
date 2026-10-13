from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]

next_event_id = 3


def find_event(event_id):
    return next(
        (event for event in events if event.id == event_id),
        None,
    )


def read_title():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return None

    return title.strip()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Events API"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    global next_event_id

    title = read_title()
    if title is None:
        return jsonify({"error": "A non-empty title is required"}), 400

    event = Event(next_event_id, title)
    events.append(event)
    next_event_id += 1

    return jsonify(event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    title = read_title()
    if title is None:
        return jsonify({"error": "A non-empty title is required"}), 400

    event.title = title
    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)