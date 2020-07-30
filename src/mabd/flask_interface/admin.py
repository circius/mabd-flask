from flask import render_template, request, url_for, Blueprint

from .. import api

from . import extensions

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
    return render_template(
        "admin_delivery_fulfilment.html",
        delivery_dict_list=delivery_dicts,
        delivery_num=delivery_id,
        error=error,
    )


@bp.route("/user_management", methods=("GET", "POST"))
@extensions.requires_auth
def user_management():
    return "to be implemented"


@bp.route("/user_management/<id>", methods=("GET", "POST"))
@extensions.requires_auth
def user_management_id(id):
    return "to be implemented"


@bp.route("/user_management/<id>/delete", methods=("GET", "POST"))
@extensions.requires_auth
def user_management_delete(id):
    return "to be implemented"


@bp.route("/user_management/add", methods=("GET", "POST"))
@extensions.requires_auth
def user_management_add():
    return "to be implemented"


@bp.route("/user_management/<id>/newlink", methods=("GET", "POST"))
@extensions.requires_auth
def user_management_newlink(id):
    return "to be implemented"
