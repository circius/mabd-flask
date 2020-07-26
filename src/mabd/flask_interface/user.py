from flask import (
    Flask,
    render_template,
    request,
    url_for,
    Blueprint,
    abort,
    redirect,
    make_response,
    flash
)

import flask_login

from .. import api

from . import forms, models

bp = Blueprint("user", __name__)


@bp.route("/")
def index():
    user_links = [
        {"link_text": "my requests", "relative_link": url_for("user.my_requests")}
    ]
    return render_template("user_index.html", links=user_links)


@bp.route("/login", endpoint="login_info", methods=['GET', 'POST'])
def login():
    form=forms.LoginForm()

    if form.validate_on_submit():
        try:
            user = models.db.session.query(
                models.User).filter(
                    models.User.username==form.username.data).one()
        except:
            message = f"invalid user {form.username.data}"
            print(message)
            flash(message)
            return redirect(url_for('user.login_info'))
        if user.check_password(form.password.data):
            flask_login.login_user(user)
            flash('successful login.')
            return redirect(url_for('user.index'))
        else:
            message = f"invalid password."
            print(message)
            flash(message)
            return redirect(url_for('user.login_info'))
    return render_template(
        "user_login_form.html",
        form=form)

@bp.route("logout")
def logout():
    flask_login.logout_user()
    flash("Successfully logged out.")
    return redirect(url_for("user.index"))


@bp.route("/myrequests")
@flask_login.login_required
def my_requests():
    airtable_username = flask_login.current_user.airtable_username
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
    )


@bp.route("/myrequests/<request_id>")
@flask_login.login_required
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
@flask_login.login_required
def matching_offer_details(request_id, offer_number):
    matching_offer = api.get_readable_offer_by_offer_number(offer_number)
    print(f"serving details for offer {offer_number}")
    return render_template(
        "matching_offer_details.html", offer=matching_offer, request_id=request_id
    )
