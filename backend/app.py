import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Event, Signup, User
from datetime import datetime
from dateutil.parser import isoparse

app = Flask(__name__)
CORS(app)

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

with app.app_context():
    db.create_all()

# -----------------------
#  POMOCNICZA FUNKCJA
# -----------------------

def find_or_create_user(username, email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
    return user

# -----------------------
#  ROUTES
# -----------------------

@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "GET":
        all_events = Event.query.all()
        result = []
        for ev in all_events:
            result.append({
                "id": ev.id,
                "title": ev.title,
                "address": ev.address,
                "date": ev.date.isoformat(),
                "capacity": ev.capacity,
                "description": ev.description,
                "creator_username": ev.creator.username if ev.creator else None,
                "creator_email": ev.creator.email if ev.creator else None
            })
        return jsonify(result), 200

    elif request.method == "POST":
        data = request.json
        raw_date = data.get("date")
        parsed_date = isoparse(raw_date) if raw_date else datetime.utcnow()

        creator_name = data.get("creator_name")
        creator_email = data.get("creator_email")
        if not creator_name or not creator_email:
            return jsonify({"error": "Musisz podać zarówno nazwę organizatora, jak i e-mail."}), 400

        user = find_or_create_user(creator_name, creator_email)

        new_event = Event(
            title=data.get("title"),
            address=data.get("address"),
            date=parsed_date,
            capacity=data.get("capacity", 10),
            description=data.get("description"),
            creator_id=user.id
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({"message": "Event created", "id": new_event.id}), 201

@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    signups_count = len(event.signups)
    free_spots = event.capacity - signups_count

    return jsonify({
        "id": event.id,
        "title": event.title,
        "address": event.address,
        "date": event.date.isoformat(),
        "description": event.description,
        "capacity": event.capacity,
        "creator_username": event.creator.username if event.creator else None,
        "creator_email": event.creator.email if event.creator else None,
        "signups_count": signups_count,
        "free_spots": free_spots
    }), 200

@app.route("/events/<int:event_id>", methods=["PUT", "DELETE"])
def update_or_delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.json

    creator_email = data.get("creator_email")
    if not creator_email:
        return jsonify({"error": "Nie podano emaila organizatora."}), 400

    user = User.query.filter_by(email=creator_email).first()
    if not user or user.id != event.creator_id:
        return jsonify({"error": "Only the creator can perform this action!"}), 403

    if request.method == "PUT":
        if data.get("title"):
            event.title = data["title"]
        if data.get("address"):
            event.address = data["address"]
        if data.get("date"):
            event.date = datetime.fromisoformat(data["date"])
        if data.get("capacity"):
            event.capacity = data["capacity"]
        if data.get("description") is not None:
            event.description = data["description"]

        db.session.commit()
        return jsonify({"message": "Event updated"}), 200

    if request.method == "DELETE":
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted"}), 200

@app.route("/events/<int:event_id>/signups", methods=["POST"])
def signup_for_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.json

    userName = data.get("name")
    userEmail = data.get("email")
    if not userName or not userEmail:
        return jsonify({"error": "Brak wymaganych danych (imię, email)."}), 400

    signups_count = len(event.signups)
    if signups_count >= event.capacity:
        return jsonify({"error": "Brak wolnych miejsc w tym wydarzeniu."}), 400

    user = find_or_create_user(userName, userEmail)

    existing_signup = Signup.query.filter_by(event_id=event.id, user_id=user.id).first()
    if existing_signup:
        return jsonify({"error": "Już jesteś zapisany na to wydarzenie."}), 400

    new_signup = Signup(event_id=event.id, user_id=user.id)
    db.session.add(new_signup)
    db.session.commit()

    return jsonify({"message": "Zapisano pomyślnie!"}), 201

# -----------------------
#  ROUTE: Dashboard
# -----------------------
@app.route("/dashboard_events", methods=["POST"])
def dashboard_events():
    """
    Odbiera email użytkownika w JSON:
    { "email": "some_user@example.com" }
    Zwraca wydarzenia utworzone przez tego użytkownika
    wraz z listą zapisanych uczestników.
    """
    data = request.json
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    events = user.events_created
    response = []
    for ev in events:
        signups_list = []
        for signup in ev.signups:
            signups_list.append({
                "username": signup.user.username,
                "email": signup.user.email
            })

        response.append({
            "event_id": ev.id,
            "title": ev.title,
            "address": ev.address,
            "date": ev.date.isoformat(),
            "description": ev.description,
            "capacity": ev.capacity,
            "signups": signups_list
        })

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
