from src.shared.definition.tables import MorningRawTable, NightRawTable
from src.web.utils import establish_mysql_connection

from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/form/morning/", methods=["GET", "POST"])
@establish_mysql_connection
def form_morning(DML=0):
    if request.method == "POST":
        result = request.form
        DML.insert(
            table=MorningRawTable,
            values=result.to_dict()
        )
        return render_template("index.html")
    else:
        return render_template("form_morning_new.html")

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/form/night/", methods=["GET", "POST"])
# def form_night():
#     return render_template("form_night_new.html")