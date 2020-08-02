import json

import os

from flask import render_template, url_for, Blueprint, redirect, flash, session, request

from six.moves.urllib.parse import urlencode

from .. import api

from . import extensions

bp = Blueprint("user", __name__)


@bp.route("/")
def index():
    user_links = [
        {"link_text": "my requests", "relative_link": url_for("user.my_requests")}
    ]
    return render_template("user_index.html", links=user_links)


@bp.route("/dashboard")
@extensions.requires_auth
def dashboard():
    return render_template(
        "dashboard.html",
        userinfo=session["profile"],
        userinfo_pretty=json.dumps(session["jwt_payload"], indent=4),
    )


@bp.route("/auth_callback")
def auth_callback(code=None):
    token = extensions.auth0.authorize_access_token()
    resp = extensions.auth0.get("userinfo")
    userinfo = resp.json()

    # print(f"token is {token}")
    # print(f"resp is {resp}")

    # Store the user information in flask session.
    session["jwt_payload"] = userinfo
    session["profile"] = {
        "user_id": userinfo["sub"],
        "name": userinfo["name"],
        "picture": userinfo["picture"],
    }
    message = f"logged in "
    flash(message)

    return redirect(url_for("user.index"))

# this DOES NOT WORK. review https://docs.authlib.org/en/latest/client/flask.html
@bp.route("/login", endpoint="login", methods=["GET", "POST"])
def login():
    am_i_deployed = os.getenv('AM_I_DEPLOYED')
    if am_i_deployed == True:
        redirect_uri = os.getenv("DEPLOYMENT_CALLBACK")
    else:
        redirect_uri = url_for("user.auth_callback", _external=True)
    return extensions.auth0.authorize_redirect(redirect_uri)


@bp.route("/logout")
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        "returnTo": url_for("user.index", _external=True),
        "client_id": "w26ToAcyeH5MUxPrg4SmB3W7ydD4fzS0",
    }
    return redirect(
        extensions.auth0.api_base_url + "/v2/logout?" + urlencode(params)
    )


@bp.route("/myrequests")
@extensions.requires_auth
def my_requests():
    airtable_username = session["profile"]["name"]
    if airtable_username == "None":
        error = "This account is misconfigured. Please contact us to sort it out."
        flash(error)
        redirect("user.index")

    requests = api.get_readable_unfulfilled_requests_of_person(airtable_username)

    requests_with_matching_offers = [
        request for request in requests if request["matching_offers_count"] > 0
    ]

    requests_no_matching_offers = [
        request for request in requests if request["matching_offers_count"] == 0
    ]

    return render_template(
        "user_requests.html",
        requests_with_offers=requests_with_matching_offers,
        requests_no_offers=requests_no_matching_offers,
        airtable_username=airtable_username,
    )


@bp.route("/myrequests/<request_id>")
@extensions.requires_auth
def matching_offers(request_id):
    requested_item_name = api.get_name_of_requested_item_from_requestID(request_id)
    matching_offer_dicts = api.get_readable_matching_offers_for_requestID(request_id)
    for d in matching_offer_dicts:
        print(d)
    return render_template(
        "matching_offers.html",
        offers=matching_offer_dicts,
        request_id=request_id,
        requested_item_name=requested_item_name,
    )


@bp.route("/myrequests/<request_id>/<offer_number>")
@extensions.requires_auth
def matching_offer_details(request_id, offer_number):
    matching_offer = api.get_readable_offer_by_offer_number(offer_number)
    return render_template(
        "matching_offer_details.html", offer=matching_offer, request_id=request_id
    )
