from flask import Flask, render_template, request, url_for, Blueprint, redirect

from .. import api

from . import models

bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
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
def user_management():
    Users = models.User.query.all()
    user_dicts = [User.get_minimal_representation() for User in Users]
    return render_template(
        "admin_user_management.html",
        user_dicts = user_dicts)

@bp.route("/user_management/<id>", methods=("GET", "POST"))
def user_management_id(id):
    this_user = models.User.query.get(id)

    if request.method == "POST":
        new_username = request.form["username"]
        new_airtable_username = request.form["airtable_username"]
        
        this_user.set_username(new_username)
        this_user.set_airtable_username(new_airtable_username)
        models.db.session.commit()

        return redirect(url_for("admin.user_management"))
    
    return render_template(
        "admin_user_management_id.html",
        user_dict = this_user.get_minimal_representation()
    )
    
@bp.route("/user_management/<id>/delete", methods=("GET", "POST"))
def user_management_delete(id):
    
    if request.method == "POST" and request.form['confirm_or_cancel'] == "confirm":
        row_to_drop = models.User.query.filter_by(id=id)        
        row_to_drop.delete()
        models.db.session.commit()
        return redirect(url_for("admin.user_management"))

    this_user = models.User.query.get(id)
    user_dict = this_user.get_minimal_representation()
    return render_template(
        "admin_user_management_delete.html",
        user_dict = user_dict
    )

@bp.route("/user_management/add", methods=("GET", "POST"))
def user_management_add():
    if request.method == "POST":
        new_username = request.form["username"]
        new_airtable_username = request.form["airtable_username"]
        new_user = models.User(username=new_username, airtable_username=new_airtable_username)
        models.db.session.add(new_user)
        models.db.session.commit()
        return redirect(url_for("admin.user_management"))
    return render_template(
    "admin_user_management_add.html")

@bp.route("/user_management/<id>/newlink", methods=("GET", "POST"))
def user_management_newlink(id):
    this_user = models.User.query.get(id)
    link = this_user.get_login_link()
    return render_template(
        "admin_user_management_newlink.html",
        link=link
    )
    
