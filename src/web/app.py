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


def login_required(f):
    def wrap(*args, **kwargs):
        if "user_id" not in session:
            flash("User not logged in", "error")
            smp.error("User not logged in")
            return redirect(url_for("unauthorized"))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/flash/<page>/<flash_category>/<message>", methods=["GET", "POST"])
def flash_message(page, flash_category, message):
    flash(message, category=flash_category)
    return render_template(f"{page}.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    smp.success("Accessing the registration page")

    if request.method == "POST":
        new_username = request.form["username"]
        new_password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        new_email = request.form["email"]

        if not ValidationUtils.is_valid_password(new_password):
            return redirect(
                url_for(
                    "flash_message",
                    page="register",
                    flash_category="error",
                    message="Password must contain at least 8 characters, 1 number, and 1 special character",
                )
            )

        if new_password != confirm_password:
            return redirect(url_for("flash_message", page="register", flash_category="error", message="Passwords do not match"))

        if not ValidationUtils.is_valid_email(new_email):
            return redirect(url_for("flash_message", page="register", flash_category="error", message="Invalid email format"))

        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            existing_user = executor.select(USERS, username=new_username)
            existing_email = executor.select(USERS, email=new_email)

            if existing_user != []:
                return redirect(url_for("flash_message", page="register", flash_category="error", message="Username already exists"))
            if existing_email != []:
                return redirect(url_for("flash_message", page="register", flash_category="error", message="Email already exists"))

            executor.insert(
                table=USERS,
                username=new_username,
                email=new_email,
                password=generate_password_hash(new_password),
                user_id=str(uuid.uuid4()),
            )

            return redirect(url_for("flash_message", page="login", flash_category="success", message="User registered successfully"))

    return render_template("accounts/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    smp.success("Accessing the login page")

    if request.method == "POST":
        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            users = executor.select(USERS, username=request.form["username"])
            user = users[0] if users else None

            if not user:
                return redirect(url_for("flash_message", page="login", flash_category="error", message="Invalid username"))
            if not check_password_hash(user.get("password"), request.form["password"]):
                return redirect(url_for("flash_message", page="login", flash_category="error", message="Invalid password"))

            session["user_id"] = user.get("user_id")
            return redirect(url_for("index"))

    return render_template("accounts/login.html")


@app.route("/logout", methods=["POST"])
def logout():
    smp.error("You are logging out")
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/unauthorized", methods=["GET"])
def unauthorized():
    smp.error("Unauthorized access attempt")
    return render_template("accounts/unauthorized.html"), 401


@app.route("/menu/entries/<entry_date>/", methods=["GET"])
@login_required
def menu_entries(entry_date):
    if not entry_date:
        return redirect(url_for("index"))

    smp.success("Accessing the Entries Menu page")

    with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
        daily_control = executor.select(
            table=DAILY_CONTROL,
            user_id=session["user_id"],
            entry_date=DateUtils.convert_date_input(date_to_convert=entry_date, format="%Y-%m-%d"),
        )

    has_data_map = {(entry["element_category"], entry["element_name"]): entry["has_data"] for entry in daily_control}

    return render_template("menu/entries.html", has_data_map=has_data_map, entry_date=entry_date)

@app.route("/menu/reports/", methods=["GET"])
@login_required
def menu_reports():
    smp.success("Accessing the Reports Menu page")
    return render_template("menu/reports.html")

@app.route("/entries/<entry_date>/<category>/<element>/", methods=["GET", "POST"])
@login_required
def upsert_entry(entry_date, category, element):
    smp.success(f"Accessing the ENTRY page with Category: {category.capitalize()} and Element: {element.capitalize()}")

    if request.method == "POST":
        smp.success(f"Processing POST request for {element.capitalize()}")

        form_data = request.form.to_dict()

        try:
            entry_date = DateUtils.convert_date_input(date_to_convert=form_data.get("date_input"))
        except ValueError as e:
            return jsonify({"message": f"Invalid date format: {e}"}), 400

        schema_fields = list(form_data.keys())

        for attempt in range(1, 4):
            try:

                with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
                    executor.upsert(
                        table=ELEMENT_ENTRIES,
                        entry_date=entry_date,
                        user_id=session["user_id"],
                        element_category=category,
                        element_name=element,
                        element_string=DictUtils.clean_and_serialize_dict(input_dict=form_data),
                        schema_encoded=ELEMENT_ENTRIES.get_schema_encoded(schema_fields=schema_fields),
                    )
                    executor.upsert(
                        table=DAILY_CONTROL,
                        entry_date=entry_date,
                        user_id=session["user_id"],
                        element_category=category,
                        element_name=element,
                        has_data=True,
                    )

                smp.success("Form successfully submitted!")
                return jsonify({"message": "Form successfully submitted!"}), 200
            except Exception as e:
                smp.error(f"Error inserting into the database on attempt {attempt}: {e}")
                time.sleep(1)

        smp.error("Error inserting into the database after multiple attempts")
        return jsonify({"message": "Error inserting into the database after multiple attempts"}), 500
    else:
        return render_template(f"entries/{category}/{element}.html", entry_date=entry_date)


@app.route("/report/<category>/<element>/", methods=["GET"])
@login_required
def report(category, element):
    smp.success(f"Accessing the REPORT page with Category: {category.capitalize()} and Element: {element.capitalize()}")

    entry_date = DateUtils.fetch_current_date_sao_paulo()
    summary_elements = [
        "navigator",
        "alchemist",
        "patron",
        "sponsor",
        "athlete",
        "diplomat",
        "citizen",
        "oracle",
        "atharva_bindu",
    ]

    if element in summary_elements:

        summary_dicts = GoldReader.summary(element=element)

        summary_dicts = filter_dictionary(dicts=summary_dicts, by="habit_action", request=request)
        summary_dicts = filter_dictionary(dicts=summary_dicts, by="habit_group", request=request)

        if not PRD:
            from pprint import pprint
            pprint(summary_dicts)

    return render_template(f"reports/{category}/{element}.html", entry_date=entry_date, summary_data=summary_dicts)


if __name__ == "__main__":
    app.run(debug=True)
