import os
import time

from flask import Flask, render_template, request, abort, jsonify

import src.shared.database.tables as tb
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.logging.adapters import reset_logger
from src.web.helpers import clean_and_serialize_dict, print_green

MAX_RETRIES = 15


reset_logger()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    print_green("Accessing the index page")
    return render_template("index.html")

@app.route("/2/", methods=["GET"])
def index2():
    print_green("Accessing the index page")
    return render_template("index2.html")

@app.route("/add/<element>/", methods=["GET", "POST"])
def add_entry(element):
    element_path = {
        "navigator": "core/wisdom",
        "sentinel": "core/wisdom",
        "sponsor": "core/stability",
        "patron": "core/stability",
        "treasurer": "core/stability",
        "nutritionist": "core/strength",
    }
    element_category = element_path[element].split("/")[1]
    
    if element not in element_path:
        abort(404)
    
    if request.method == "POST":
        print_green(f"Processing POST request for {element.capitalize()}")
        
        retry_count = 1        
        form_data = request.form.to_dict()
        date = form_data["date_input"]
        prepared_data = clean_and_serialize_dict(data=form_data)

        while retry_count < MAX_RETRIES:
            try:
                with DatabaseExecutorBuilder() as executor:
                    executor.insert(
                        table=tb.ElementEntries, 
                        date=date,
                        user_id=1,
                        element_category=element_category,
                        element_name=element,
                        element_string=prepared_data,
                        op="c",
                    )
                break
            except Exception as e:
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Error inserting into the database after multiple attempts", 500
        else:
            return render_template(f"{element_path[element]}/{element}.html")
    else:
        return render_template(f"{element_path[element]}/{element}.html")

@app.route("/form/morning/", methods=["GET", "POST"])
def form_morning():
    print_green("Accessing the morning form page")
    table = tb.MySqlMorningTable
    if request.method == "POST":
        retry_count = 1
        prepared_data = clean_and_serialize_dict(data=request.form.to_dict())
        while retry_count < MAX_RETRIES:
            try:
                with DatabaseExecutorBuilder() as executor:
                    executor.insert(table, data=prepared_data, profile="heuschmat")
                break
            except Exception as e:
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
    print_green("Accessing the night form page")
    table = tb.MySqlNightTable
    if request.method == "POST":
        retry_count = 1
        prepared_data = clean_and_serialize_dict(data=request.form.to_dict())
        while retry_count < MAX_RETRIES:
            try:
                with DatabaseExecutorBuilder() as executor:
                    executor.insert(table, data=prepared_data, profile="heuschmat")
                break
            except Exception as e:
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Error inserting into the database after multiple attempts", 500
        else:
            return render_template("index.html")
    else:
        return render_template("night.html")


@app.route("/test/", methods=["GET", "POST"])
def form_test():
    print_green("Accessing the test form page")
    table = tb.LocalTest
    if request.method == "POST":
        retry_count = 1
        prepared_data = clean_and_serialize_dict(data=request.form.to_dict())
        while retry_count < MAX_RETRIES:
            try:
                with DatabaseExecutorBuilder() as executor:
                    executor.insert(table, data=prepared_data, profile="heuschmat")
                break
            except Exception as e:
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
