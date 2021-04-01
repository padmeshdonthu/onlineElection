import hashlib
import json
from collections import namedtuple

import requests
from flask import Blueprint, render_template, request, flash, session, url_for
from werkzeug.utils import redirect

from online_election.access_secmanager import SecretManager
from online_election.user_management.User import UserDetails
from online_election.user_management.emailService import send_email

bp = Blueprint('register', __name__, template_folder="templates", static_folder="static")


def json_decoder(user_dictionary):
    return namedtuple('X', user_dictionary.keys())(*user_dictionary.values())


def fetch_secret_key(secret_name, key_name):
    secret = SecretManager().get_secret(secret_name, key_name)
    return secret


@bp.route("/register", methods=['GET'])
def get_register_page():
    return render_template("register.html")


@bp.route("/register", methods=['POST'])
def submit_data():
    first_name = str(request.form.get("first_name", ""))
    last_name = str(request.form.get("last_name", ""))
    password = str(request.form.get("password", ""))
    confirm_password = str(request.form.get("confirm_password", ""))
    phone = str(request.form.get("phone", ""))
    email = str(request.form.get("email", ""))
    user = UserDetails(first_name, last_name, password, phone, email)

    if first_name == "" or last_name == "" or password == "" or phone == "" or email == "":
        flash("One or more fields are empty!!! Please try again!")
        return render_template("register.html")
    if password != confirm_password:
        flash("The passwords are not matching!! Please try again!!")
        return render_template("register.html")
    else:
        # 1. get details from dynamodb for the email id. If exists, throw error
        # 2. If not existing, insert to dynamodb and also encrypt the password
        # 3. Once inserted, send an email with a verification code
        # 4. Render a template which verifies that verification code
        secret_name = "usermgmt/usrmgmtkey"
        key_name = "UsermgmtAPIKey"
        secret = fetch_secret_key(secret_name, key_name)
        get_user_url = "https://as5r1zw6c8.execute-api.us-east-1.amazonaws.com/test/usermanagement"
        add_user_url = "https://as5r1zw6c8.execute-api.us-east-1.amazonaws.com/test/usermanagement"

        headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
        params = {"email_id": user.email}
        user.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        add_user_params = {
            "email_id": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password,
            "phone": user.phone,
            "verified": user.verified
        }

        response = requests.get(get_user_url, params=params, headers=headers)
        print(response.text)
        if "Unauthorized" in response.text or "Forbidden" in response.text:
            return redirect(url_for("error.get_unauthorized_error_page"))

        user_details = json.loads(response.text, object_hook=json_decoder)

        if not bool(user_details):
            response = requests.post(add_user_url, json=add_user_params, headers=headers)
            if "Unauthorized" in response.text or "Forbidden" in response.text:
                return redirect(url_for("error.get_unauthorized_error_page"))
            generated_otp = send_email(user.email, user.first_name + ' ' + user.last_name)
            session["email_id"] = user.email
            session["otp"] = generated_otp
            return render_template("verify_email_address.html")
        else:
            flash("The user already exists in the system. Please login instead!")
            return render_template("register.html")


@bp.route("/verify_email_address", methods=['POST'])
def verify_email_address():
    secret_name = "usermgmt/usrmgmtkey"
    key_name = "UsermgmtAPIKey"
    secret = fetch_secret_key(secret_name, key_name)
    entered_code = str(request.form.get("code", ""))
    if session["otp"] != entered_code:
        flash("The entered code is incorrect!")
        return render_template("verify_email_address.html")
    else:
        # Call a Lambda to update the user as verified!
        update_verified_status_url = "https://as5r1zw6c8.execute-api.us-east-1.amazonaws.com/test/verifyuser"
        headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}

        update_user_verification = {
            "email_id": session["email_id"],
            "verified": "Y"
        }
        response = requests.post(update_verified_status_url, json=update_user_verification, headers=headers)
        if "Unauthorized" in response.text or "Forbidden" in response.text:
            return redirect(url_for("error.get_unauthorized_error_page"))
        print(response.text)
        secret_name = "snsmgmt/snsmgmtkey"
        key_name = "SnsMgmtAPIKey"
        secret1 = fetch_secret_key(secret_name, key_name)
        headers = {"Content-type": "application/json", "x-api-key": secret1, "authorizationToken": secret1}
        send_email_params = {
            "email_id": session["email_id"]
        }
        send_email_url = "https://hqk1etk2nl.execute-api.us-east-1.amazonaws.com/test/snsmanagement"
        response = requests.post(send_email_url, json=send_email_params, headers=headers)
        print(response.text)
        if "Unauthorized" in response.text or "Forbidden" in response.text:
            return redirect(url_for("error.get_unauthorized_error_page"))
        session.pop("email_id", None)
        session.pop("otp", None)
        return redirect(url_for("login.get_login_page"))
