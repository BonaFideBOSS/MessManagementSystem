from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from . import db
import base64
from bson import ObjectId

db = db.db
manager = Blueprint("manager", __name__)


@manager.before_request
def is_user_admin():
    if not any(role in session["user"]["roles"] for role in ["admin"]):
        return redirect(url_for("auth.login"))


@manager.route("/")
def dashboard():
    food_count = db.Foods.count_documents({})
    user_count = db.Users.count_documents({})
    data = {"food_count": food_count, "user_count": user_count}
    return render_template("manager/dashboard.html", data=data)


@manager.route("/orders")
def orders():
    pipeline = [
        {"$group": {"_id": "$food_id", "quantity": {"$sum": 1}}},
        {"$sort": {"quantity": -1}},
        {
            "$lookup": {
                "from": "Foods",
                "localField": "_id",
                "foreignField": "_id",
                "as": "food_info",
            }
        },
    ]
    orders = list(db.Orders.aggregate(pipeline))
    return render_template("manager/orders.html", orders=orders)


@manager.route("/foods")
def foods():
    foods = db.Foods.find({})
    return render_template("manager/foods.html", foods=foods)


@manager.route("/foods/new", methods=["GET", "POST"])
def new_food():
    if request.method == "POST":
        try:
            food = {
                "name": request.form.get("name"),
                "credits": int(request.form.get("credits")),
                "image": convert_img_to_base64(request.files.get("image")),
            }
            db.Foods.insert_one(food)
            flash("Successfully add a new food.")
            return redirect(url_for("manager.foods"))
        except:
            flash("Failed to add new food.")

    return render_template("manager/new-food.html")


@manager.route("/foods/delete/<food_id>", methods=["POST"])
def delete_food(food_id):
    try:
        db.Foods.delete_one({"_id": ObjectId(food_id)})
        db.Orders.delete_many({"food_id": ObjectId(food_id)})
        flash("Successfully deleted food.")
    except:
        flash("Failed to delete food")
    return redirect(request.referrer)


@manager.route("/users")
def users():
    return render_template("manager/users.html")


def convert_img_to_base64(image):
    image = image.read()
    image = base64.b64encode(image).decode("utf-8")
    image = f"data:image/*;base64,{image}"
    return image
