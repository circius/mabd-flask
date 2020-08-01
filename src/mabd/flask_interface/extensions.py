import json

from functools import wraps

from flask import session, redirect
from . import mabd_secrets

from authlib.integrations.flask_client import OAuth

oauth = OAuth()

auth0 = oauth.register("auth0") # get settings from app.config


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "profile" not in session:
            # Redirect to Login page here
            return redirect("/")
        return f(*args, **kwargs)

    return decorated


def must_be_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user_email = session["jwt_payload"]["email"]
        if current_user_email not in mabd_secrets.admin_emails_list:
            print(f"{current_user_email} not in {mabd_secrets.admin_emails_list}")
            return redirect("/")
        return f(*args, **kwargs)

    return decorated
