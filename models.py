from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Pilot(UserMixin, db.Model):
    __tablename__ = 'pilot'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    date_joined = db.Column(db.DateTime, server_default=db.func.now())
    hangar = db.relationship('Aircraft', backref='owner', lazy=True)

class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    icao_code = db.Column(db.String(10), nullable=False)
    registration = db.Column(db.String(16), unique=True, nullable=False)
    purchased_date = db.Column(db.DateTime, server_default=db.func.now())
    location = db.Column(db.String(16), default="")
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilot.id'), nullable=False)