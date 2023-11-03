from flask import Blueprint, render_template
from . import db

db = db.db
views = Blueprint("views", __name__)


@views.route("/")
def home():
    user_count = db.Users.find({})
    return render_template("home.html")
