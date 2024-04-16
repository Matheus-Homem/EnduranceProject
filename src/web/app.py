from src.shared.connections.builder import Connector, build_connection
from src.shared.definition.statements import DataManipulationLanguage
from src.shared.definition.tables import MorningRawTable, NightRawTable

from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


ssh_connection = build_connection(
    connection_type=Connector.SSH,
)
mysql_connection = build_connection(
    connection_type=Connector.MYSQL,
    tunnel=ssh_connection,
)

DML = DataManipulationLanguage(connection=mysql_connection)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# @app.route("/form/night/", methods=["GET", "POST"])
# def form_night():
#     return render_template("form_night_new.html")

@app.route("/form/morning/", methods=["GET", "POST"])
def form_morning():
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