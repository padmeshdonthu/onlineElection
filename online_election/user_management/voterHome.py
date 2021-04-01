from flask import Blueprint, render_template, session, flash

bp = Blueprint('voterHome', __name__, template_folder="templates", static_folder="static")


@bp.route("/voterHome", methods=["GET"])
def get_voter_home():
    if "email_id" not in session:
        return render_template("voter_home.html")
    if "message" in session:
        flash(session["message"])
        session.pop("message", None)
    return render_template("voter_home.html")
