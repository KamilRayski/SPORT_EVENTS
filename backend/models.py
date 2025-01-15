from datetime import datetime
from database import db

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)  # Nowy atrybut: adres
    latitude = db.Column(db.Float, nullable=True)        # Koordynaty
    longitude = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, default=10)

    creator_name = db.Column(db.String(100), nullable=False)  # Organizator (uprośćmy)

    signups = db.relationship("Signup", backref="event", cascade="all, delete", lazy=True)

class Signup(db.Model):
    __tablename__ = "signups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
