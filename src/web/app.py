import os
import time

from flask import Flask, render_template, request

import src.shared.database.tables as tb
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.logger import LoggingManager
from src.web.helpers import clean_and_serialize_dict

MAX_RETRIES = 15

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    logger = LoggingManager().get_logger()
    logger.info("Accessing the index page")
    return render_template("index.html")


@app.route("/form/morning/", methods=["GET", "POST"])
def form_morning():
    logger = LoggingManager().get_logger()
    logger.info("Accessing the morning form page")
    table = tb.MySqlMorningTable
    if request.method == "POST":
        logger.info("Receiving POST request")
        retry_count = 1
        prepared_data = clean_and_serialize_dict(data=request.form.to_dict())
        while retry_count < MAX_RETRIES:
            logger.info(
                f"Trying to insert data into table {table.__tablename__}. Attempt: {retry_count}"
            )
            try:
                with DatabaseExecutorBuilder() as executor:
                    executor.insert(table, data=prepared_data, profile="heuschmat")
                break
            except Exception as e:
                logger.error(
                    f"Error inserting into the database with data {prepared_data} on attempt {retry_count}: {e}",
                    exc_info=True,
                )
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            logger.error(f"Error inserting into the database after multiple attempts")
            return "Error inserting into the database after multiple attempts", 500
        else:
            logger.info("Returning to index page")
            return render_template("index.html")
    else:
        return render_template("morning.html")


@app.route("/form/night/", methods=["GET", "POST"])
def form_night():
    logger = LoggingManager().get_logger()
    logger.info("Accessing the night form page")
    table = tb.MySqlNightTable
    if request.method == "POST":
        logger.info("Receiving POST request")
        retry_count = 1
        prepared_data = clean_and_serialize_dict(data=request.form.to_dict())
        while retry_count < MAX_RETRIES:
            logger.info(
                f"Trying to insert data into table {table.__tablename__}. Attempt: {retry_count}"
            )
            try:
                with DatabaseExecutorBuilder() as executor:
                    executor.insert(table, data=prepared_data, profile="heuschmat")
                break
            except Exception as e:
                logger.error(
                    f"Error inserting into the database with data {prepared_data} on attempt {retry_count}: {e}",
                    exc_info=True,
                )
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            logger.error(f"Error inserting into the database after multiple attempts")
            return "Error inserting into the database after multiple attempts", 500
        else:
            logger.info("Returning to index page")
            return render_template("index.html")
    else:
        return render_template("night.html")


@app.route("/test/", methods=["GET", "POST"])
def form_test():
    logging_manager = LoggingManager()
    logger = logging_manager.get_logger()
    table = tb.LocalTest
    logger.info("Accessing the test form page")
    if request.method == "POST":
        logger.info("Receiving POST request")
        retry_count = 1
        prepared_data = clean_and_serialize_dict(data=request.form.to_dict())
        while retry_count < MAX_RETRIES:
            logger.info(
                f"Trying to insert data into table {table.__tablename__}. Attempt: {retry_count}"
            )
            try:
                with DatabaseExecutorBuilder() as executor:
                    executor.insert(table, data=prepared_data, profile="heuschmat")
                break
            except Exception as e:
                logger.error(
                    f"Error inserting into the database with data {prepared_data} on attempt {retry_count}: {e}",
                    exc_info=True,
                )
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            logger.error(f"Error inserting into the database after multiple attempts")
            return "Error inserting into the database after multiple attempts", 500
        else:
            logger.info("Returning to index page")
            return render_template("index.html")
    else:
        return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
