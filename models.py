from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Pilot(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, server_default=db.func.now())
    fleets = db.relationship('Fleet', backref='manager', lazy=True)
    logbook = db.relationship('PilotFlightLog', backref='pilot', lazy=True)

class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilot.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    home_base_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=True)
    hangars = db.relationship('Hangar', backref='fleet', lazy=True)
    offices = db.relationship('Office', backref='fleet', lazy=True)
    aircraft = db.relationship('Aircraft', backref='fleet', lazy=True)
    flights = db.relationship('Flight', backref='fleet', lazy=True)
    fees = db.relationship('Fee', backref='fleet', lazy=True)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, default="CJX Aviation")
    balance = db.Column(db.Float, default=0.0)
    hq_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=True)
    storage_id = db.Column(db.Integer, db.ForeignKey('hangar.id'), nullable=True)
    financial_logs = db.relationship('CompanyFinancialLog', backref='company', lazy=True)
    flights = db.relationship('Flight', backref='company', lazy=True)

class Aircraft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    icao_code = db.Column(db.String(10), nullable=False)
    registration = db.Column(db.String(16), unique=True, nullable=False)
    purchased_date = db.Column(db.DateTime, server_default=db.func.now())
    location = db.Column(db.String(16), default="")
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=True)
    hangar_id = db.Column(db.Integer, db.ForeignKey('hangar.id'), nullable=True)
    maintenance = db.relationship('Maintenance', backref='aircraft', lazy=True)
    flights = db.relationship('Flight', backref='aircraft', lazy=True)

class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icao = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=True)
    fleets = db.relationship('Fleet', backref='home_base', lazy=True)
    hangars = db.relationship('Hangar', backref='airport', lazy=True)
    offices = db.relationship('Office', backref='airport', lazy=True)

class Hangar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=True)
    company_owned = db.Column(db.Boolean, default=False)
    aircraft = db.relationship('Aircraft', backref='hangar', lazy=True)

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=True)
    company_owned = db.Column(db.Boolean, default=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    lease_percent = db.Column(db.Float, nullable=False, default=0.10)
    from_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=True)
    to_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=True)
    pilotlogs = db.relationship('PilotFlightLog', backref='flight', lazy=True)

class PilotFlightLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilot.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    role = db.Column(db.String(32), nullable=True) # PIC, SIC, etc.

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(128), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    paid_by_company = db.Column(db.Boolean, default=True)

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(32), nullable=False)  # storage, landing, FBO, etc.
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(128), nullable=True)

class CompanyFinancialLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)