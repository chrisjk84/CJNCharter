from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Pilot(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag

    # Add your other fields as needed

class Aircraft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(32), unique=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    # Add your other fields as needed

# (Optional) Add Fleet, Company, Financial models as you need.