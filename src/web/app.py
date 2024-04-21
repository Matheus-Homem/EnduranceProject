from src.web.utils import establish_mysql_connection

from flask import Flask, render_template, request
from datetime import datetime
import json
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/form/morning/", methods=["GET", "POST"])
@establish_mysql_connection
def form_morning(cursor):
    if request.method == "POST":
        date_id = datetime.now().strftime("%Y%m%d")
        data = request.form.to_dict()
        data_json = json.dumps(data)
        cursor.execute(f"INSERT INTO RawMorning (id, data) VALUES ('{date_id}', '{data_json}')")
        return render_template("index.html")
    else:
        return render_template("form_morning_new.html")

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/form/night/", methods=["GET", "POST"])
# def form_night():
#     return render_template("form_night_new.html") 