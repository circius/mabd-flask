from flask import Flask, render_template, request, url_for, Blueprint

from .. import api

bp = Blueprint("admin", __name__)


@bp.route("/")
def index():
    links_to_provide = [
        {
            "link_text": "delivery fulfilment",
            "relative_link": url_for("admin.fulfil_deliveries"),
        }
    ]
    return render_template("admin_index.html", links=links_to_provide)


@bp.route("/fulfilment")
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
