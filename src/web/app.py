from src.env.credentials import Credentials
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

# Use environment variable for MONGO_URI if it"s set, otherwise use the local URI
app.config["MONGO_URI"] = Credentials.MONGO_URI

mongo = PyMongo(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/form/night/", methods=["GET", "POST"])
def form_night():
    return render_template("form_night_new.html")

@app.route("/form/morning/", methods=["GET", "POST"])
def form_morning():
    if request.method == "POST":
        result = request.form
        mongo.db.morning_form.insert_one(result.to_dict())
        return render_template("index.html")
    else:
        return render_template("form_morning_new.html")

if __name__ == "__main__":
    app.run(debug=True)