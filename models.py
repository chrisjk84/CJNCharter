from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    aircraft = db.relationship('Aircraft', backref='fleet', lazy=True)
    pilots = db.relationship('Pilot', backref='fleet', lazy=True)

class Aircraft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(32), unique=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=True)

class Pilot(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_grounded = db.Column(db.Boolean, default=False)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=True)

class CompanyFinancial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    revenue = db.Column(db.Float, default=0.0)
    expenses = db.Column(db.Float, default=0.0)