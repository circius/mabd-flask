import json, pprint, urllib

from flask import render_template, request, url_for, Blueprint, redirect, flash

from .. import api

from . import extensions, auth0

bp = Blueprint("admin", __name__)


@bp.route("/")
@extensions.requires_auth
@extensions.must_be_admin
def index():
    links_to_provide = [
        {
            "link_text": "delivery fulfilment",
            "relative_link": url_for("admin.fulfil_deliveries"),
        },
        {
            "link_text": "user management",
            "relative_link": url_for("admin.user_management"),
        },
    ]
    return render_template("admin_index.html", links=links_to_provide)


@bp.route("/fulfilment")
@extensions.requires_auth
def fulfil_deliveries():
    error = None
    delivery_id = request.args.get("delivery_id", default=-1, type=int)
    if delivery_id != -1:
        result = api.do_delivery_fulfilment(delivery_id)
        if result is False:
            error = f"No unfulfilled delivery has the number {delivery_id}"
    delivery_dicts = api.get_readable_unfulfilled_deliveries()
    flash(error)
    return render_template(
        "admin_delivery_fulfilment.html",
        delivery_dict_list=delivery_dicts,
        delivery_num=delivery_id,
    )


@bp.route("/user_management", methods=("GET", "POST"))
@extensions.requires_auth
@extensions.must_be_admin
def user_management():
    useful_keys = ["user_id", "email", "nickname", "app_metadata"]

    def user_get_useful_subset(userdict):
        result_dict = {k: None for k in useful_keys}
        for key in userdict.keys():
            if key in result_dict.keys():
                result_dict[key] = userdict[key]
        result_dict["user_id_urlsafe"] = result_dict["user_id"].replace("|", "%7C")
        return result_dict

    def users_get_useful_subset(users):
        return [user_get_useful_subset(userdict) for userdict in users]

    users = auth0.auth0.users.list()
    userlist = users["users"]
    useful_users_data = users_get_useful_subset(userlist)
    do_not_show_in_table = ["user_id", "user_id_urlsafe"]

    return render_template(
        "admin_user_management.html",
        user_dicts=useful_users_data,
        do_not_show_in_table=do_not_show_in_table,
    )


@bp.route("/user_management/<urlsafe_id>", methods=("GET", "POST"))
@extensions.requires_auth
@extensions.must_be_admin
def user_management_id(urlsafe_id):
    auth0_id = urlsafe_id.replace("%7C", "|")

    def update_user(id, nickname, airtable_username):
        update_body = {
            "nickname": nickname,
            "app_metadata": {"airtable_username": airtable_username},
        }
        auth0.auth0.users.update(id, update_body)

    if request.method == "POST":
        nickname = request.form["nickname"]
        airtable_username = request.form["airtable_username"]
        update_user(auth0_id, nickname, airtable_username)

        return redirect(url_for("admin.user_management"))

    required_fields = ["user_id", "email", "nickname", "app_metadata"]
    current_user_data = auth0.auth0.users.get(
        auth0_id, fields=required_fields, include_fields=True
    )
    if "app_metadata" not in current_user_data.keys():
        current_user_data["app_metadata"] = None
    return render_template("admin_user_management_id.html", user_dict=current_user_data)


@bp.route("/user_management/<urlsafe_id>/delete", methods=("GET", "POST"))
@extensions.requires_auth
@extensions.must_be_admin
def user_management_delete(urlsafe_id):
    auth0_id = urlsafe_id.replace("%7C", "|")
    if request.method == "POST":
        if request.form["confirm_or_cancel"] == "confirm":
            auth0.auth0.users.delete(auth0_id)
        return redirect(url_for("admin.user_management"))

    user_email = auth0.auth0.users.get(auth0_id)["email"]
    print(user_email)
    return render_template(
        "admin_user_management_delete.html", user_id=auth0_id, user_email=user_email
    )


@bp.route("/user_management/add", methods=("GET", "POST"))
@extensions.requires_auth
@extensions.must_be_admin
def user_management_add():
    def add_user(email, nickname, airtable_username):
        create_body = {
            "email": email,
            "nickname": nickname,
            "app_metadata": {"airtable_username": airtable_username},
            "connection": "email",
        }
        return auth0.auth0.users.create(create_body)

    if request.method == "POST":
        email = request.form["email"]
        nickname = request.form["nickname"]
        airtable_username = request.form["airtable_username"]
        new_user = add_user(email, nickname, airtable_username)
        return redirect(url_for("admin.user_management"))

    return render_template("admin_user_management_add.html")


@bp.route("/user_management/<id>/newlink", methods=("GET", "POST"))
@extensions.requires_auth
@extensions.must_be_admin
def user_management_newlink(id):
    return "to be implemented"
