from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .forms import RegisterForm, LoginForm, encrypt_message
from bson import json_util

db = db.db
auth = Blueprint("auth", __name__)


@auth.before_request
def is_user_logged_in():
    if "user" in session and request.endpoint != "auth.logout":
        return redirect(url_for("views.home"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        data = form.data
        data.pop("csrf_token")
        data["password"] = encrypt_message(data["password"])
        db.Users.insert_one(data)
        flash("Successfully created new account. Please login to continue.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.Users.find_one({"email": form.email.data})
        user["_id"] = json_util.dumps(user["_id"]).split('"')[3]
        session["user"] = user
        session.permanent = True if request.form.get("remember") == "on" else False
        flash("Successfully logged in.")
        return redirect(url_for("views.home"))

    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    flash("Successfully logged out.")
    return redirect(url_for("auth.login"))
