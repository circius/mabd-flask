from flask import (
    Flask,
    render_template,
    request,
    url_for,
    Blueprint,
    abort,
    redirect,
    make_response,
)

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
def do_login(username):
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

    requests = api.get_readable_unfulfilled_requests_of_person(current_user)

    requests_with_matching_offers = [
        request for request in requests if request["matching_offers_count"] > 0
    ]

    requests_no_matching_offers = [
        request for request in requests if request["matching_offers_count"] == 0
    ]

    return render_template(
        "user_requests.html",
        current_user=current_user,
        requests_with_offers=requests_with_matching_offers,
        requests_no_offers=requests_no_matching_offers,
    )


@bp.route("/myrequests/<request_id>")
def matching_offers(request_id):
    requested_item_name = api.get_name_of_requested_item_from_requestID(request_id)
    matching_offer_dicts = api.get_readable_matching_offers_for_requestID(request_id)
    return render_template(
        "matching_offers.html",
        offers=matching_offer_dicts,
        request_id=request_id,
        requested_item_name=requested_item_name,
    )


@bp.route("/myrequests/<request_id>/<offer_uid>")
def matching_offer_details(request_id, offer_uid):
    matching_offer = api.get_readable_offer_by_offer_uid(offer_uid)

    return render_template(
        "matching_offer_details.html", offer=matching_offer, request_id=request_id
    )
