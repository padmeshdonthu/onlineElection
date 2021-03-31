import json
import time
from collections import namedtuple
from datetime import date

import requests
from flask import Blueprint, session, render_template, request, jsonify, url_for
from werkzeug.utils import redirect

from online_election.access_secmanager import SecretManager
from online_election.voting_management.Election import Election

bp = Blueprint('elections', __name__, template_folder="templates", static_folder="static")


def json_decoder(user_dictionary):
    return namedtuple('X', user_dictionary.keys())(*user_dictionary.values())


@bp.route("/ongoing", methods=["GET"])
def get_ongoing_elections():
    if "email_id" not in session:
        return render_template("ongoing_election_list.html")
    secret_name = "electionmgmt/electionmgmtkey"
    key_name = "ElectionMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    get_elections_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/votingmanagement"
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    params = {"email_id": session["email_id"]}

    response = requests.get(get_elections_url, params=params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    election_list_response = json.loads(response.text, object_hook=json_decoder)
    print(election_list_response)
    submitted_elections = election_list_response.submittedElections
    elections = []
    for election_item in election_list_response.elections:
        election = Election(election_item.election_id, election_item.election_type,
                            election_item.election_text,
                            election_item.election_title,
                            election_item.election_candidates,
                            election_item.start_date, election_item.end_date,
                            election_item.results_published)
        elections.append(election)

    # filter elections that are already submitted by the user
    if len(submitted_elections) > 0:
        submitted_elections = [x for x in submitted_elections
                               if x.voter_id == session["email_id"]]
        election_id_list = [o.election_id for o in submitted_elections]
        print(election_id_list)
        elections = [y for y in elections if y.election_id not in election_id_list]
        print(submitted_elections)

    # filter out the elections that have not yet started or already over!

    date_formatted = date.today().strftime("%d/%m/%Y")
    elections = [x for x in elections if
                 time.strptime(x.start_date, "%d/%m/%Y") <= time.strptime(date_formatted, "%d/%m/%Y")
                 <= time.strptime(x.end_date, "%d/%m/%Y")]
    elections = [x for x in elections if x.results_published == "N"]

    return render_template("ongoing_election_list.html", election_list=elections, len=len(elections))


@bp.route("/submitted", methods=["GET"])
def get_submitted_elections():
    if "email_id" not in session:
        return render_template("submitted_election_list.html")
    secret_name = "electionmgmt/electionmgmtkey"
    key_name = "ElectionMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    get_elections_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/votingmanagement"
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    params = {"email_id": session["email_id"]}

    response = requests.get(get_elections_url, params=params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    election_list_response = json.loads(response.text, object_hook=json_decoder)
    print(election_list_response)
    submitted_elections = election_list_response.submittedElections
    elections = []
    for election_item in election_list_response.elections:
        election = Election(election_item.election_id, election_item.election_type,
                            election_item.election_text,
                            election_item.election_title,
                            election_item.election_candidates,
                            election_item.start_date, election_item.end_date,
                            election_item.results_published)
        elections.append(election)

    # filter elections that are already submitted by the user
    if len(submitted_elections) > 0:
        submitted_elections = [x for x in submitted_elections
                               if x.voter_id == session["email_id"]]
        election_id_list = [o.election_id for o in submitted_elections]
        print(election_id_list)
        elections = [y for y in elections if y.election_id in election_id_list]
        print(submitted_elections)
    else:
        elections = []
    return render_template("submitted_election_list.html", election_list=elections, len=len(elections),
                           submitted_elections=submitted_elections,
                           submitted_len=len(submitted_elections))


@bp.route('/castVote/<string:election_id>', methods=['GET'])
def get_cast_vote_page(election_id):
    if "email_id" not in session:
        return render_template("create_election.html")
    get_election_by_id_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/electionmanagement"
    secret_name = "electionmgmt/electionmgmtkey"
    key_name = "ElectionMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    params = {"election_id": election_id}
    response = requests.get(get_election_by_id_url, params=params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    election_details = json.loads(response.text, object_hook=json_decoder)
    return render_template("cast_election.html", election=election_details,
                           len=len(election_details.election_candidates))


@bp.route("/castVote", methods=["POST"])
def cast_vote():
    if "email_id" not in session:
        return render_template("cast_election.html")
    option = request.form.getlist('candidate_group')
    election_id = request.form.get("election_id", "")
    print(option)
    print(election_id)
    secret_name = "electionmgmt/electionmgmtkey"
    key_name = "ElectionMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    cast_your_vote_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/votingmanagement"
    cast_vote_params = {
        "email_id": session["email_id"],
        "election_id": election_id,
        "status": "voted",
        "vote_date": date.today().strftime("%d/%m/%Y"),
        "candidate_voted": option[0]
    }
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}

    response = requests.post(cast_your_vote_url, json=cast_vote_params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    details = json.loads(response.text)
    session["message"] = "Successfully created the election!"
    # sns mail must be sent
    secret_name = "snsmgmt/snsmgmtkey"
    key_name = "SnsMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    email_list = []
    email_list.append(session['email_id'])
    publish_email_params = {
        "email_id" : email_list,
        "message"  : "You have successfully casted your valuable vote. Please wait for the annoucement email for the results"
    }
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    publish_email_url = "https://hqk1etk2nl.execute-api.us-east-1.amazonaws.com/test/publishmessage"
    response = requests.post(publish_email_url, json=publish_email_params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    return redirect(url_for("voterHome.get_voter_home"))


@bp.route('/findWinner', methods=['GET'])
def find_winner():
    if "email_id" not in session:
        render_template("submitted_election_list.html")
    election_id = request.args.get('election_id')
    get_submitted_votes_url = "https://s9uztjegil.execute-api.us-east-1.amazonaws.com/test/resultsmanagement"
    secret_name = "electionmgmt/electionmgmtkey"
    key_name = "ElectionMgmtAPIKey"
    secret = SecretManager().get_secret(secret_name, key_name)
    headers = {"Content-type": "application/json", "x-api-key": secret, "authorizationToken": secret}
    params = {"election_id": election_id}
    response = requests.get(get_submitted_votes_url, params=params, headers=headers)
    if "Unauthorized" in response.text or "Forbidden" in response.text:
        return redirect(url_for("error.get_unauthorized_error_page"))
    election_details = json.loads(response.text, object_hook=json_decoder)
    results_dictionary = {}
    for item in election_details:
        if item.candidate_voted in results_dictionary:
            results_dictionary[item.candidate_voted] += 1
        else:
            results_dictionary[item.candidate_voted] = 1

    max_value = 0
    for key in results_dictionary:
        if results_dictionary[key] > max_value:
            max_value = results_dictionary[key]

    winning_candidate = []
    for key in results_dictionary:
        if results_dictionary[key] == max_value:
            winning_candidate.append(key)

    tie = False
    empty = False
    if len(winning_candidate) > 1:
        tie = True
        empty = False

    if len(winning_candidate) == 0:
        empty = True

    return jsonify({'winner': winning_candidate, 'tie': tie, 'empty': empty})
