from flask import Flask, render_template, request, url_for, Blueprint, abort

from .. import api

bp = Blueprint("user", __name__)


@bp.route("/")
def index():
    user_links = [
        {"link_text": "my requests", "relative_link": url_for("user.my_requests")}
    ]
    return render_template("user_index.html", links=user_links)


@bp.route("/myrequests")
def my_requests():
    try:
        current_user = request.cookies["user"]
    except:
        abort(403)

    current_requests = ["mockrequest1", "mockrequest2"]
    return render_template(
        "user_requests.html", user=current_user, requests=current_requests
    )


@bp.route("/myrequests/request_id")
def matching_offers():
    matching_offers = ["mockoffer1", "mockoffer2"]
    return render_template("matching_offers.html", offers=matching_offers)
