import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Event, Signup
from datetime import datetime
from dateutil.parser import isoparse

app = Flask(__name__)
CORS(app)

# Odczytujemy konfigurację bazy z ENV
db_user = os.environ.get("DATABASE_USER", "postgres")
db_password = os.environ.get("DATABASE_PASSWORD", "secret")
db_host = os.environ.get("DATABASE_HOST", "db")
db_port = os.environ.get("DATABASE_PORT", "5432")
db_name = os.environ.get("DATABASE_NAME", "sports_db")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Tworzymy tabele przy starcie
with app.app_context():
    db.create_all()

# -----------------------
#  ROUTES
# -----------------------

@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "GET":
        # Zwracamy listę wydarzeń
        all_events = Event.query.all()
        result = []
        for ev in all_events:
            result.append({
                "id": ev.id,
                "title": ev.title,
                "address": ev.address,
                "latitude": ev.latitude,
                "longitude": ev.longitude,
                "date": ev.date.isoformat(),
                "capacity": ev.capacity,
                "creator_name": ev.creator_name,
                "description": ev.description
                # możesz dodać też np. licznik signups
            })
        return jsonify(result), 200

    elif request.method == "POST":
        # Tworzymy nowe wydarzenie
        data = request.json
        raw_date = data.get("date")
        # Parsujemy datę z isoparse, jeśli istnieje, w przeciwnym razie używamy datetime.utcnow()
        parsed_date = isoparse(raw_date) if raw_date else datetime.utcnow()

        new_event = Event(
            title=data.get("title"),
            address=data.get("address"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            date=parsed_date,
            capacity=data.get("capacity", 10),
            creator_name=data.get("creator_name", "Anon"),
            description=data.get("description")
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({"message": "Event created", "id": new_event.id}), 201

@app.route("/events/<int:event_id>", methods=["PUT", "DELETE"])
def update_or_delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == "PUT":
        data = request.json
        # Sprawdź, czy user to twórca
        if data.get("creator_name") != event.creator_name:
            return jsonify({"error": "Only the creator can edit!"}), 403
        
        event.title = data.get("title", event.title)
        event.address = data.get("address", event.address)
        event.latitude = data.get("latitude", event.latitude)
        event.longitude = data.get("longitude", event.longitude)
        if data.get("date"):
            event.date = datetime.fromisoformat(data["date"])
        event.capacity = data.get("capacity", event.capacity)
        event.description = data.get("description", event.description)
        db.session.commit()
        return jsonify({"message": "Event updated"}), 200

    if request.method == "DELETE":
        data = request.json
        # Sprawdź, czy user to twórca
        if data.get("creator_name") != event.creator_name:
            return jsonify({"error": "Only the creator can delete!"}), 403

        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted"}), 200

@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    # Zliczamy ilu jest zapisanych
    signups_count = len(event.signups)
    free_spots = event.capacity - signups_count
    return jsonify({
        "id": event.id,
        "title": event.title,
        "address": event.address,
        "latitude": event.latitude,
        "longitude": event.longitude,
        "date": event.date.isoformat(),
        "description": event.description,
        "capacity": event.capacity,
        "creator_name": event.creator_name,
        "signups_count": signups_count,
        "free_spots": free_spots
    }), 200


if __name__ == "__main__":
    # Odpalamy na porcie 8000
    app.run(debug=True, host="0.0.0.0", port=8000)
