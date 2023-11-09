from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from . import db
from bson import ObjectId
from datetime import datetime

db = db.db
user = Blueprint("user", __name__)


@user.before_request
def is_user_logged_in():
    if not "user" in session:
        return redirect(url_for("auth.login"))


@user.route("/menu")
def menu():
    foods = db.Foods.find({})
    return render_template("menu.html", foods=foods)


@user.route("/order/<food_id>", methods=["POST"])
def order(food_id):
    try:
        food = db.Foods.find_one({"_id": ObjectId(food_id)})
        user = session["user"]
        if user["credits"] >= food["credits"]:
            db.Orders.insert_one(
                {
                    "user_id": ObjectId(user["_id"]),
                    "food_id": food["_id"],
                    "date": datetime.now(),
                }
            )
            user_credits = user["credits"] - food["credits"]
            db.Users.update_one(
                {"_id": ObjectId(user["_id"])},
                {"$set": {"credits": user_credits}},
            )
            session['user']['credits'] = user_credits
            flash("Successfully placed order!")
        else:
            flash("You do not have enough credits.")
    except Exception as e:
        print(e)
        flash("Failed to place order.")
    return redirect(url_for("user.menu"))
