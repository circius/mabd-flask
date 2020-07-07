from flask import Flask, render_template, request, url_for, Blueprint, abort

from .. import api

bp = Blueprint("user", __name__)


@bp.route("/")
def index():
    user = request.cookies.get("user")
    if user is not None:
        print("someone is logged in")
    user_links = [
        {"link_text": "my requests", "relative_link": url_for("user.my_requests")}
    ]
    return render_template("user_index.html", links=user_links, user=user)


@bp.route("/login", endpoint="login_info")
def login():
    return render_template("user_login.html")


@bp.route("/login/<username>", endpoint="do_login")
def login(username):
    response = make_response(redirect(url_for("user.index")))
    response.set_cookie("user", username)
    return response


@bp.route("logout")
def logout():
    response = make_response(redirect(url_for("user.index")))
    response.delete_cookie("user")
    return response


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
