from src.web.utils import establish_mysql_connection

from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
import os
import time

MAX_RETRIES = 2
load_dotenv( )
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/form/morning/", methods=["GET", "POST"])
@establish_mysql_connection
def form_morning(cursor):
    if request.method == "POST":
        data = request.form.to_dict()
        data_json = json.dumps(data)
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                cursor.execute(f"INSERT INTO RawMorning (data) VALUES ('{data_json}');")
                break
            except Exception as e:
                print(f"Erro ao inserir no banco de dados: {e}")
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Erro ao inserir no banco de dados após várias tentativas", 500
        else:
            return render_template("index.html")
    else:
        return render_template("form_morning_new.html")

@app.route("/form/night/", methods=["GET", "POST"])
#@establish_mysql_connection
def form_night(cursor=None):
    # TODO: FIX THIS TO WORK PROPERLY
    if request.method == "POST":
        data = request.form.to_dict()
        data_json = json.dumps(data)
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                cursor.execute(f"INSERT INTO RawNight (data) VALUES ('{data_json}');")
                break
            except Exception as e:
                print(f"Erro ao inserir no banco de dados: {e}")
                retry_count += 1
                time.sleep(1)
        if retry_count == MAX_RETRIES:
            return "Erro ao inserir no banco de dados após várias tentativas", 500
        else:
            return render_template("index.html")
    else:
        return render_template("form_night_new.html")
    
if __name__ == "__main__":
    app.run(debug=True)