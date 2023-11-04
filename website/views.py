from flask import Blueprint, render_template
from . import db

db = db.db
views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/about")
def about():
    return render_template("about.html")
