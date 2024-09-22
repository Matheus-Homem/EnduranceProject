import os
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
from werkzeug.security import check_password_hash, generate_password_hash

import src.shared.database.tables as tb
from src.shared.credentials import PRD
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.utils import DateUtils, DictUtils, HashUtils, ValidationUtils
from src.web.helpers import SimpleMessagePrinter as smp

MAX_RETRIES = 15

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_secret_key")


def login_required(f):
    def wrap(*args, **kwargs):
        if "user_id" not in session:
            flash("User not logged in", "error")
            smp.error("User not logged in")
            return redirect(url_for("unauthorized"))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


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
            existing_user = executor.select(tb.Users, username=new_username)
            existing_email = executor.select(tb.Users, email=new_email)

            if existing_user != []:
                return redirect(url_for("flash_message", page="register", flash_category="error", message="Username already exists"))
            if existing_email != []:
                return redirect(url_for("flash_message", page="register", flash_category="error", message="Email already exists"))

            executor.insert(
                table=tb.Users,
                username=new_username,
                email=new_email,
                password=generate_password_hash(new_password),
                user_id=str(uuid.uuid4()),
            )

            return redirect(url_for("flash_message", page="login", flash_category="success", message="User registered successfully"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    smp.success("Accessing the login page")

    if request.method == "POST":
        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            users = executor.select(tb.Users, username=request.form["username"])
            user = users[0] if users else None

            if not user:
                return redirect(url_for("flash_message", page="login", flash_category="error", message="Invalid username"))
            if not check_password_hash(user.get("password"), request.form["password"]):
                return redirect(url_for("flash_message", page="login", flash_category="error", message="Invalid password"))

            session["user_id"] = user.get("user_id")
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    smp.error("You are logging out")
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/unauthorized", methods=["GET"])
def unauthorized():
    smp.error("Unauthorized access attempt")
    return render_template("unauthorized.html"), 401


@app.route("/", methods=["GET"])
@login_required
def index():
    smp.success("Accessing the index page")
    return render_template("index.html")


@app.route("/add/<category>/<element>/", methods=["GET", "POST"])
@login_required
def add_entry(category, element):
    smp.success(f"Accessing the entry page with Category: {category.capitalize()} and Element: {element.capitalize()}")
    element_entries_table = tb.ElementEntries

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
                        table=element_entries_table,
                        uc_name=element_entries_table.get_unique_constraint_name(),
                        date=entry_date,
                        user_id=session["user_id"],
                        element_category=category,
                        element_name=element,
                        element_string=DictUtils.clean_and_serialize_dict(data=form_data),
                        schema_hash=element_entries_table.get_schema_hash(schema_fields=schema_fields),
                    )

                smp.success("Form successfully submitted!")
                return jsonify({"message": "Form successfully submitted!"}), 200
            except Exception as e:
                smp.error(f"Error inserting into the database on attempt {attempt}: {e}")
                time.sleep(1)

        smp.error("Error inserting into the database after multiple attempts")
        return jsonify({"message": "Error inserting into the database after multiple attempts"}), 500
    else:
        return render_template(f"core/{category}/{element}.html")


if __name__ == "__main__":
    app.run(debug=True)
