from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from database.database import db
from database.models import User
from utils.validators import ValidationError, require_email, require_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            if not name:
                raise ValidationError("Name is required.")
            email = require_email(request.form.get("email", ""))
            password = require_password(request.form.get("password", ""))

            if User.query.filter_by(email=email).first():
                raise ValidationError("An account with this email already exists.")

            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash("Account created successfully.", "success")
            return redirect(url_for("index"))

        except ValidationError as exc:
            flash(str(exc), "danger")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=request.form.get("remember") == "on")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
