import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, Pilot, Aircraft, Fleet, CompanyFinancial

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cjx_pilots.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Pilot.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def create_admin():
    admin = Pilot.query.filter_by(username="admin").first()
    if not admin:
        admin = Pilot(
            username="admin",
            email="admin@company.com",
            password_hash=generate_password_hash("password"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', pilot=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        if not username or not email or not password:
            flash("All fields are required.", "error")
        elif Pilot.query.filter((Pilot.username == username) | (Pilot.email == email)).first():
            flash("Username or email already exists.", "error")
        else:
            new_pilot = Pilot(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(new_pilot)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password']
        pilot = Pilot.query.filter((Pilot.username == username) | (Pilot.email == username)).first()
        if pilot and check_password_hash(pilot.password_hash, password):
            login_user(pilot)
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username/email or password.", "error")
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

# --- Admin Dashboard ---
@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    pilots = Pilot.query.all()
    aircraft = Aircraft.query.all()
    fleets = Fleet.query.all()
    financial = CompanyFinancial.query.first()
    return render_template("admin_dashboard.html", pilots=pilots, aircraft=aircraft, fleets=fleets, financial=financial)

# --- Aircraft CRUD ---
@app.route("/admin/aircraft/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_aircraft():
    fleets = Fleet.query.all()
    if request.method == "POST":
        registration = request.form["registration"]
        type_ = request.form["type"]
        fleet_id = request.form.get("fleet_id") or None
        aircraft = Aircraft(registration=registration, type=type_, fleet_id=fleet_id)
        db.session.add(aircraft)
        db.session.commit()
        flash("Aircraft added!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("add_aircraft.html", fleets=fleets)

@app.route("/admin/aircraft/<int:aircraft_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_aircraft(aircraft_id):
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    fleets = Fleet.query.all()
    if request.method == "POST":
        aircraft.registration = request.form["registration"]
        aircraft.type = request.form["type"]
        aircraft.fleet_id = request.form.get("fleet_id") or None
        db.session.commit()
        flash("Aircraft updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_aircraft.html", aircraft=aircraft, fleets=fleets)

# --- Fleet CRUD ---
@app.route("/admin/fleet/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_fleet():
    if request.method == "POST":
        name = request.form["name"]
        fleet = Fleet(name=name)
        db.session.add(fleet)
        db.session.commit()
        flash("Fleet added!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("add_fleet.html")

@app.route("/admin/fleet/<int:fleet_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_fleet(fleet_id):
    fleet = Fleet.query.get_or_404(fleet_id)
    if request.method == "POST":
        fleet.name = request.form["name"]
        db.session.commit()
        flash("Fleet updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_fleet.html", fleet=fleet)

# --- Assign Pilot to Fleet ---
@app.route("/admin/pilot/<int:pilot_id>/assign_fleet", methods=["GET", "POST"])
@login_required
@admin_required
def assign_pilot_fleet(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)
    fleets = Fleet.query.all()
    if request.method == "POST":
        pilot.fleet_id = request.form.get("fleet_id") or None
        db.session.commit()
        flash("Pilot assigned to fleet!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("assign_pilot_fleet.html", pilot=pilot, fleets=fleets)

# --- Remove or Ground Pilot ---
@app.route("/admin/pilot/<int:pilot_id>/ground", methods=["POST"])
@login_required
@admin_required
def ground_pilot(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)
    pilot.is_grounded = True
    db.session.commit()
    flash("Pilot grounded.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/pilot/<int:pilot_id>/remove", methods=["POST"])
@login_required
@admin_required
def remove_pilot(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)
    db.session.delete(pilot)
    db.session.commit()
    flash("Pilot removed.", "success")
    return redirect(url_for("admin_dashboard"))

# --- Edit Company Financials ---
@app.route("/admin/company_financials/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_company_financials():
    financial = CompanyFinancial.query.first()
    if not financial:
        financial = CompanyFinancial()
        db.session.add(financial)
        db.session.commit()
    if request.method == "POST":
        financial.balance = float(request.form["balance"])
        financial.revenue = float(request.form["revenue"])
        financial.expenses = float(request.form["expenses"])
        db.session.commit()
        flash("Company financials updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_company_financials.html", financial=financial)

# --- Edit Pilot (username/email/is_admin) ---
@app.route("/admin/pilot/<int:pilot_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_pilot(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)
    if request.method == "POST":
        pilot.username = request.form["username"]
        pilot.email = request.form["email"]
        pilot.is_admin = "is_admin" in request.form
        db.session.commit()
        flash("Pilot updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_pilot.html", pilot=pilot)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)