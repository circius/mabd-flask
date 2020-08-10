import json

import os

from flask import render_template, url_for, Blueprint, redirect, flash, session, request

from six.moves.urllib.parse import urlencode

from .. import api

from . import extensions, auth0

bp = Blueprint("user", __name__)


@bp.route("/")
def index():
    user_links = [
        {"link_text": "my requests", "relative_link": url_for("user.my_requests")}
    ]
    return render_template("user_index.html", links=user_links)


@bp.route("/auth_callback")
def auth_callback():
    token = extensions.auth0.authorize_access_token()
    resp = extensions.auth0.get("userinfo")
    userinfo = resp.json()

    # Store the user information in flask session.
    session["jwt_payload"] = userinfo
    session["profile"] = {
        "user_id": userinfo["sub"],
        "name": userinfo["name"],
        "picture": userinfo["picture"],
    }
    message = "logged in"
    flash(message)

    return redirect(url_for("user.index"))


@bp.route("/login", endpoint="login", methods=["GET", "POST"])
def login():
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
    return redirect(extensions.auth0.api_base_url + "/v2/logout?" + urlencode(params))


@bp.route("/myrequests")
@extensions.requires_auth
def my_requests():
    airtable_username = session["profile"]["name"]

    try:
        requests = api.get_readable_unfulfilled_requests_of_person(airtable_username)
    except:
        error = "This account is misconfigured. Please contact us to sort it out."
        flash(error)
        redirect("user.index")

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
    confirmed_offer_dict = api.get_readable_confirmed_offer_for_requestID(request_id)
    matching_offer_dicts = api.get_readable_matching_offers_for_requestID(request_id)

    return render_template(
        "matching_offers.html",
        offers=matching_offer_dicts,
        request_id=request_id,
        requested_item_name=requested_item_name,
        confirmed_offer_dict=confirmed_offer_dict,
    )


@bp.route("/myrequests/<request_id>/<offer_number>/<action>")
@extensions.requires_auth
def matching_offer_perform_action(request_id, offer_number, action):
    airtable_username = session["profile"]["name"]

    if action == "accept":
        result = api.do_offer_confirmation(request_id, offer_number)

    elif action == "reject":
        result = api.do_offer_rejection(request_id, offer_number)

    if result == False:
        flash("There was an error; we could not complete the requested action.")

    return redirect(url_for("user.matching_offers", request_id=request_id))


@bp.route("/myrequests/<request_id>/<offer_number>")
@extensions.requires_auth
def matching_offer_details(request_id, offer_number):
    matching_offer = api.get_readable_offer_by_offer_number(offer_number)
    return render_template(
        "matching_offer_details.html", offer=matching_offer, request_id=request_id
    )
