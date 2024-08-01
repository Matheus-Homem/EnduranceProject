import os
import time

from flask import Flask, render_template, request

from src.shared.logger import Logger
from src.shared.handlers import MySqlHandler
from src.web.functions import prepare_dict_to_command

MAX_RETRIES = 2

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/form/morning/", methods=["GET", "POST"])
def form_morning():
    if request.method == "POST":
        retry_count = 0
        prepared_data = prepare_dict_to_command(data=request.form.to_dict())
        statement = f"INSERT INTO morning_data (data) VALUES ('{prepared_data}');"
        while retry_count < MAX_RETRIES:
            try:
                MySqlHandler().execute(statement=statement)
                break
            except Exception as e:
                print(f"Error inserting into the database: {e}")
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Error inserting into the database after multiple attempts", 500
        else:
            return render_template("index.html")
    else:
        return render_template("morning.html")


@app.route("/form/night/", methods=["GET", "POST"])
def form_night():
    if request.method == "POST":
        retry_count = 0
        prepared_data = prepare_dict_to_command(data=request.form.to_dict())
        statement = f"INSERT INTO night_data (data) VALUES ('{prepared_data}');"
        while retry_count < MAX_RETRIES:
            try:
                print(prepared_data)
                MySqlHandler().execute(statement=statement)
                break
            except Exception as e:
                print(f"Error inserting into the database: {e}")
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Error inserting into the database after multiple attempts", 500
        else:
            return render_template("index.html")
    else:
        return render_template("night.html")
    
@app.route("/test/", methods=["GET", "POST"])
def form_morning():
    if request.method == "POST":
        retry_count = 0
        prepared_data = prepare_dict_to_command(data=request.form.to_dict())
        statement = f"INSERT INTO local_test (data) VALUES ('{prepared_data}');"
        while retry_count < MAX_RETRIES:
            try:
                MySqlHandler().execute(statement=statement)
                break
            except Exception as e:
                print(f"Error inserting into the database: {e}")
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Error inserting into the database after multiple attempts", 500
        else:
            return render_template("index.html")
    else:
        return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
