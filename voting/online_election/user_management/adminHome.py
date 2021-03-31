from flask import Blueprint, render_template, flash
from flask import session

bp = Blueprint('adminHome', __name__, template_folder="templates", static_folder="static")


@bp.route("/adminHome", methods=["GET"])
def get_admin_home():
    if "email_id" not in session:
        return render_template("admin_home.html")
    if "message" in session:
        flash(session["message"])
        session.pop("message", None)
    return render_template("admin_home.html")
