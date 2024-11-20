import time
import uuid

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_caching import Cache
from werkzeug.security import check_password_hash, generate_password_hash

from os_local import get_environment_variable
from src.database.connection.builder import DatabaseExecutorBuilder
from src.database.tables import DailyControl, ElementEntries, Users
from src.shared.credentials import PRD
from src.shared.report.reader import GoldReader
from src.shared.utils import DateUtils, DictUtils, ValidationUtils
from src.web.helpers import SimpleMessagePrinter as smp
from src.web.helpers import filter_dictionary

MAX_RETRIES = 15
ELEMENT_ENTRIES = ElementEntries
DAILY_CONTROL = DailyControl
USERS = Users

app = Flask(__name__)
app.config["SECRET_KEY"] = get_environment_variable(var="SECRET_KEY", default="default_secret_key")
app.config["CACHE_TYPE"] = "simple"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

cache = Cache(app)

### A cada escolha uma renuncia

@app.route("/")
def index():
    return render_template("index2.html")

if __name__ == "__main__":
    app.run(debug=True)
