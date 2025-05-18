import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Pilot, Aircraft  # Add other models as needed

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

# --- Company Financials Page ---
@app.route("/company_financials")
@login_required
def company_financials():
    # Example: get data, e.g. CompanyFinancialLog.query.all()
    # For now, just render the template
    return render_template("company_financials.html")

# --- Company Flight Log Page ---
@app.route("/company_flightlog")
@login_required
def company_flightlog():
    # Example: get flight log data here if available
    return render_template("company_flightlog.html")

# --- Fleets Overview ---
@app.route("/fleets")
@login_required
def fleets():
    return render_template("fleets.html")

# --- Fleet Assets ---
@app.route("/fleet_assets")
@login_required
def fleet_assets():
    return render_template("fleet_assets.html")

# --- Fleet Details ---
@app.route("/fleet_details")
@login_required
def fleet_details():
    return render_template("fleet_details.html")

# --- Fleet Flight Log ---
@app.route("/fleet_flightlog")
@login_required
def fleet_flightlog():
    return render_template("fleet_flightlog.html")

# --- Pilots Overview ---
@app.route("/pilots")
@login_required
def pilots():
    return render_template("pilots.html")

# --- Pilot Logbook ---
@app.route("/pilot_logbook")
@login_required
def pilot_logbook():
    return render_template("pilot_logbook.html")

# --- Error Handler for 404 ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Only run db.create_all() for local development
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)