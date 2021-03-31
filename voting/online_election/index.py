from flask import Blueprint, render_template, session, url_for
from werkzeug.utils import redirect

bp = Blueprint('index', __name__, template_folder="templates", static_folder="static")


@bp.route("/", methods=["GET"])
def get_index_page():
    if "email_id" in session:
        return redirect(url_for("voterHome.get_voter_home"))
    else:
        return render_template("index.html")
