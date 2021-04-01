from flask import (
    Blueprint, render_template
)

bp = Blueprint('error', __name__, template_folder="templates", static_folder="static")


@bp.route("/error", methods=['GET'])
def get_unauthorized_error_page():
    return render_template("error.html")
