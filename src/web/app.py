import os
import time

from flask import Flask, jsonify, render_template, request

import src.shared.database.tables as tb
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.logging.adapters import reset_logger
from src.web.helpers import (
    clean_and_serialize_dict,
    convert_input_date,
    display_debug_message,
    display_error_message,
    display_success_message,
)

MAX_RETRIES = 15


reset_logger()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    display_success_message("Accessing the index page")
    return render_template("index.html")


@app.route("/2/", methods=["GET"])
def index2():
    display_success_message("Accessing the index page")
    return render_template("index2.html")


@app.route("/add/<category>/<element>/", methods=["GET", "POST"])
def add_entry(category, element):

    display_debug_message(f"Received element = {element}")
    display_debug_message(f"Received category = {category}")

    if request.method == "POST":
        display_success_message(f"Processing POST request for {element.capitalize()}")

        form_data = request.form.to_dict()
        display_debug_message(f"Form data received: {form_data}")

        try:
            entry_date = convert_input_date(date_to_convert=form_data.get("date_input"))
        except ValueError as e:
            return jsonify({"message": f"Invalid date format: {e}"}), 400

        entry_string = clean_and_serialize_dict(data=form_data)
        display_debug_message(f"Serialized entry string: {entry_string}")

        for attempt in range(1, 4):
            try:
                with DatabaseExecutorBuilder(use_production_db=True) as executor:
                    executor.insert(
                        table=tb.ElementEntries,
                        date=entry_date,
                        user_id=1,
                        element_category=category,
                        element_name=element,
                        element_string=entry_string,
                        schema_version=1,
                        op="c",
                    )
                display_success_message("Form successfully submitted!")
                return jsonify({"message": "Form successfully submitted!"}), 200
            except Exception as e:
                display_error_message(f"Error inserting into the database on attempt {attempt}: {e}")
                time.sleep(1)

        display_error_message("Error inserting into the database after multiple attempts")
        return jsonify({"message": "Error inserting into the database after multiple attempts"}), 500
    else:
        return render_template(f"core/{category}/{element}.html")


@app.route("/form/morning/", methods=["GET", "POST"])
def form_morning():
    display_success_message("Accessing the morning form page")
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
    display_success_message("Accessing the night form page")
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
    display_success_message("Accessing the test form page")
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
