import os
import time

from flask import Flask, jsonify, render_template, request

import src.shared.database.tables as tb
from src.shared.credentials import PRD
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


@app.route("/add/<category>/<element>/", methods=["GET", "POST"])
def add_entry(category, element):

    display_debug_message(f"Received element = {element}")
    display_debug_message(f"Received category = {category}")

    element_entries_table = tb.ElementEntries

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
                with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
                    executor.upsert(
                        table=element_entries_table,
                        uc_name=element_entries_table.get_unique_constraint_name(),
                        date=entry_date,
                        user_id=1,
                        element_category=category,
                        element_name=element,
                        element_string=entry_string,
                        schema_version=1,
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


if __name__ == "__main__":
    app.run(debug=True)
