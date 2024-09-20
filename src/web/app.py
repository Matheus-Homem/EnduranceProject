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
from src.shared.logging.adapters import reset_logger
from src.web.helpers import (
    clean_and_serialize_dict,
    convert_input_date,
    display_debug_message,
    display_error_message,
    display_success_message,
    is_valid_email,
    is_valid_password,
)

MAX_RETRIES = 15


reset_logger()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_secret_key")


@app.route("/", methods=["GET"])
def index():

    if "user_id" not in session:
        display_error_message("User not logged in")
        return redirect(url_for("unauthorized"))

    display_success_message("Accessing the index page")
    return render_template("index.html")


@app.route("/unauthorized", methods=["GET"])
def unauthorized():
    display_error_message("Unauthorized access attempt")
    return render_template("unauthorized.html"), 401


@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user_id"):
        display_debug_message("User already logged in")
    else:
        display_debug_message("User not logged in")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with DatabaseExecutorBuilder(use_production_db=False) as executor:
            user = executor.select(tb.User, username=username)[0] if executor.select(tb.User, username=username) else None

            if user and check_password_hash(user.get("password"), password):
                session["user_id"] = user.get("user_id")
                flash("Login successful!", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    display_debug_message("You are logging out")
    session.pop("user_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    display_success_message("Accessing the registration page")

    if request.method == "POST":
        new_username = request.form["username"]
        new_password = request.form["password"]
        new_email = request.form["email"]

        if not is_valid_password(new_password):
            display_error_message("Password must contain at least 8 characters, 1 number, and 1 special character")
            return jsonify({"error": "Password must contain at least 8 characters, 1 number, and 1 special character"}), 400

        if not is_valid_email(new_email):
            display_error_message("Invalid email format")
            return jsonify({"error": "Invalid email format"}), 400

        hashed_password = generate_password_hash(new_password)

        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            existing_user = executor.select(tb.User, username=new_username)
            existing_email = executor.select(tb.User, email=new_email)
            if existing_user != []:
                flash("Username already exists", "danger")
            elif existing_email != []:
                flash("Email already exists", "danger")
            else:
                executor.insert(table=tb.User, username=new_username, email=new_email, password=hashed_password, user_id=str(uuid.uuid4()))
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/add/<category>/<element>/", methods=["GET", "POST"])
def add_entry(category, element):

    if "user_id" not in session:
        display_error_message("User not logged in")
        return redirect(url_for("unauthorized"))

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

        user_id = session["user_id"]

        for attempt in range(1, 4):
            try:
                with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
                    executor.upsert(
                        table=element_entries_table,
                        uc_name=element_entries_table.get_unique_constraint_name(),
                        date=entry_date,
                        user_id=user_id,
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
