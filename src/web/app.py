from src.shared.database.operations import DatabaseOperations
from src.web.utils import prepare_form_data

from flask import Flask, render_template, request
import os
import time

MAX_RETRIES = 2

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/form/morning/", methods=["GET", "POST"])
def form_morning():
    if request.method == "POST":
        prepared_data = prepare_form_data(data=request.form.to_dict())
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                DatabaseOperations.execute_command(
                    f"INSERT INTO morning_data (data) VALUES ('{prepared_data}');"
                )
                break
            except Exception as e:
                print(f"Erro ao inserir no banco de dados: {e}")
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
        prepared_data = prepare_form_data(data=request.form.to_dict())
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                DatabaseOperations.execute_command(
                    f"INSERT INTO night_data (data) VALUES ('{prepared_data}');"
                )
                break
            except Exception as e:
                print(f"Erro ao inserir no banco de dados: {e}")
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Error inserting into the database after multiple attempts", 500
        else:
            return render_template("index.html")
    else:
        return render_template("night.html")


if __name__ == "__main__":
    app.run(debug=True)
