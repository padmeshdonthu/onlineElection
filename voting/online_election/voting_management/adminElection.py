import json
import time
import uuid
from collections import namedtuple
from datetime import date

import requests
from flask import Blueprint, render_template, request, flash, session, url_for
from werkzeug.utils import redirect

from online_election.access_secmanager import SecretManager
from online_election.voting_management.Candidate import Candidate
from online_election.voting_management.Election import Election

bp = Blueprint('adminElection', __name__, template_folder="templates", static_folder="static")


def json_decoder(user_dictionary):
    return namedtuple('X', user_dictionary.keys())(*user_dictionary.values())


def fetch_secret_key():
    secret_name = "electionmgmt/electionmgmtkey"
    key_name = "ElectionMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    return secret


@bp.route("/viewElections", methods=["GET"])
def view_elections():
    if "email_id" not in session:
        return render_template("admin_election_list.html")
    secret = fetch_secret_key()
    get_elections_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/votingmanagement"
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    params = {"email_id": session["email_id"]}

    response = requests.get(get_elections_url, params=params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    election_list_response = json.loads(response.text, object_hook=json_decoder)
    elections = []
    for election_item in election_list_response.elections:

        can_publish = "N"
        if time.strptime(date.today().strftime("%d/%m/%Y"), "%d/%m/%Y") > time.strptime(election_item.end_date,
                                                                                        "%d/%m/%Y"):
            can_publish = "Y"

        election = Election(election_item.election_id, election_item.election_type,
                            election_item.election_text,
                            election_item.election_title,
                            election_item.election_candidates,
                            election_item.start_date, election_item.end_date,
                            election_item.results_published, can_publish)
        elections.append(election)

    if "message" in session:
        flash(session["message"])
        session.pop("message", None)
    return render_template("admin_election_list.html", election_list=elections, len=len(elections))


@bp.route("/createElection", methods=["GET"])
def create_election():
    return render_template("create_election.html")


@bp.route("/saveElectionDetails", methods=["POST"])
def submit_data():
    if "email_id" not in session:
        return render_template("create_election.html")

    election_type = str(request.form.get("election_type", ""))
    election_title = str(request.form.get("election_title", ""))
    election_text = str(request.form.get("election_text", ""))
    election_start_date = (request.form.get("start_date", ""))
    election_end_date = (request.form.get("end_date", ""))
    election_candidate_name = request.form.getlist("candidate")
    election_candidate_party = request.form.getlist("candidate_party")
    newdate1 = time.strptime(election_start_date, "%d/%m/%Y")
    newdate2 = time.strptime(election_end_date, "%d/%m/%Y")

    if election_type == "":
        flash("Election type is required!!")
        return render_template("create_election.html")
    if election_title == "":
        flash("Election title is required!!")
        return render_template("create_election.html")
    if election_text == "":
        flash("Election description is required!!")
        return render_template("create_election.html")
    if election_start_date is None:
        flash("Election start date is required!!")
        return render_template("create_election.html")
    if election_end_date is None:
        flash("Election end date is required!!")
        return render_template("create_election.html")
    if election_candidate_name is None or election_candidate_party is None:
        flash("Two or more candidates must be included in the election in order to cast a vote!")
        return render_template("create_election.html")
    if len(election_candidate_name) <= 1 or len(election_candidate_party) <= 1:
        flash("Two or more candidates must be included in the election in order to cast a vote!")
        return render_template("create_election.html")
    if newdate1 >= newdate2:
        flash("The start date must be less than the end date!!")
        return render_template("create_election.html")

    candidate_list = []

    for i, j in zip(election_candidate_name, election_candidate_party):
        candidate = Candidate(str(i), str(j))
        candidate_list.append(candidate)

    election_id = str(uuid.uuid4())
    election = Election(election_id, election_type, election_text, election_title, candidate_list,
                        election_start_date, election_end_date, "N")
    print(str(election))
    secret = fetch_secret_key()
    create_election_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/electionmanagement"
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    serialized_election = json.dumps(election, default=lambda o: o.__dict__)
    print(serialized_election)
    response = requests.post(create_election_url, data=serialized_election, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    print(response.text)
    session["message"] = "Successfully created the election!"
    return redirect(url_for("adminHome.get_admin_home"))


@bp.route('/publishElection/<string:election_id>', methods=['GET'])
def publish_election(election_id):
    if "email_id" not in session:
        return redirect(url_for("adminElection.view_elections"))
    print(election_id)
    secret = fetch_secret_key()
    publish_election_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/resultsmanagement"
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    response = requests.post(publish_election_url, json={"election_id": election_id}, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    print(response.text)
    session["message"] = "Successfully published the election!"
    # sns mail must be sent
    send_mail_lst = []
    resp = requests.get(publish_election_url, params={"election_id": election_id}, headers=headers)
    for record in eval(resp.text):
        send_mail_lst .append(record['voter_id'])
    secret_name = "snsmgmt/snsmgmtkey"
    key_name = "SnsMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    publish_email_params = {
        "email_id" : send_mail_lst,
        "message"  : "Results are out for the elections for which you have voted as a responsible citizen"
    }
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    publish_email_url = "https://hqk1etk2nl.execute-api.us-east-1.amazonaws.com/test/publishmessage"
    response = requests.post(publish_email_url, json=publish_email_params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))    


    return redirect(url_for("adminElection.view_elections"))
