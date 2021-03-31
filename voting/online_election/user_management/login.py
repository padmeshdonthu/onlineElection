import hashlib
import json
from collections import namedtuple

import requests
from flask import (
    Blueprint, render_template, request, flash, session, url_for
)
from werkzeug.utils import redirect

from online_election.access_secmanager import SecretManager
from online_election.user_management.User import UserDetails

bp = Blueprint('login', __name__, template_folder="templates", static_folder="static")


@bp.route("/login", methods=['GET'])
def get_login_page():
    if 'email' in session:
        return 'Logged in as {}'.format(session['email_id'])
    return render_template("login.html")


def json_decoder(user_dictionary):
    return namedtuple('X', user_dictionary.keys())(*user_dictionary.values())


def fetch_secret_key():
    secret_name = "usermgmt/usrmgmtkey"
    key_name = "UsermgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    return secret


@bp.route("/login", methods=['POST'])
def submit_data():
    email = str(request.form.get("email", ""))
    password = str(request.form.get("password", ""))
    hashed_pwd = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = UserDetails(first_name='', last_name='', phone='', email=email, password=hashed_pwd)

    if email == "" or password == "":
        flash("One or more fields are empty!!! Please try again!")
        return render_template("login.html")
    else:
        # fetch data from dynamo for the user, if does not exist, redirect to register page fetch data from dynamo
        # for the user, if exists, check for the verified field, if verified redirect to home page
        secret = fetch_secret_key()
        session['email_id'] = user.email
        if str(user.email).lower() == "noreply.horizon.group1@gmail.com":
            session["role"] = "ADMIN"
        else:
            session["role"] = "USER"
        get_user_url = "https://as5r1zw6c8.execute-api.us-east-1.amazonaws.com/test/usermanagement"
        headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
        params = {"email_id": user.email}

        response = requests.get(get_user_url, params=params, headers=headers)
        print(response.text)
        if "Unauthorized" in response.text or "Forbidden" in response.text:
            return redirect(url_for("error.get_unauthorized_error_page"))
        user_details = json.loads(response.text, object_hook=json_decoder)

        validate_details = {
            'email_id': user.email,
            'password': user.password
        }
        validate_user_url = "https://as5r1zw6c8.execute-api.us-east-1.amazonaws.com/test/login"

        if bool(user_details):
            # check for verification code and match the password
            response = requests.post(validate_user_url, json=validate_details, headers=headers)
            if response.text == 'Invalid email_id':
                flash('Incorrect password. Try Again')
                return render_template('login.html')
            elif response.text == 'Email not verified':
                flash('Email id not verified')
                return render_template('login.html')
            elif "email_id" in response.text:
                if session["role"] == "USER":
                    return redirect(url_for("voterHome.get_voter_home"))
                else:
                    return redirect(url_for("adminHome.get_admin_home"))
            elif "Unauthorized" in response.text or "Forbidden" in response.text:
                return redirect(url_for("error.get_unauthorized_error_page"))
        else:
            flash("The user does not exist. Please register instead!")
            return render_template("register.html")


@bp.route('/logout')
def logout():
    # remove the email from the session if it is present 
    session.pop('email_id', None)
    session.pop("role", None)
    session.clear()
    return redirect(url_for("login.get_login_page"))
