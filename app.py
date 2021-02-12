import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/tasks")
def tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()}
        )

        if existing_user:
            print("Email Already Taken")
            return redirect(url_for("register"))

        register = {
            "first_name": request.form.get("first name").lower(),
            "last_name": request.form.get("last name").lower(),
            "passowrd": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower()
            print("Registration Completed")
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("first name", "last name").lower()
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
