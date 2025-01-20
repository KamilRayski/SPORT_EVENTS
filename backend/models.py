from datetime import datetime
from database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=True, default="")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, default=10)

    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    creator = db.relationship("User", backref="events_created", lazy=True)

    signups = db.relationship("Signup", backref="event", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<Event id={self.id} title={self.title} creator_id={self.creator_id}>"

class Signup(db.Model):
    __tablename__ = "signups"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="signups", lazy=True)

    def __repr__(self):
        return f"<Signup id={self.id} event_id={self.event_id} user_id={self.user_id}>"
