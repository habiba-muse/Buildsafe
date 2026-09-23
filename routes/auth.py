from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User, Assessment

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with that email already exists.")
            return redirect(url_for("auth.register"))

        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created. Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.")
            return redirect(url_for("auth.login"))

        session["user_id"] = user.id
        return redirect(url_for("auth.dashboard"))

    return render_template("login.html")

@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    assessments = Assessment.query.filter_by(user_id=user.id).order_by(Assessment.created_at.desc()).all()
    return render_template("dashboard.html", user=user, assessments=assessments)

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
