from functools import wraps

from flask import session, redirect

from authlib.integrations.flask_client import OAuth

# from auth0.v3.management import Auth0

oauth = OAuth()

auth0 = oauth.register(
    "auth0",
    client_id="w26ToAcyeH5MUxPrg4SmB3W7ydD4fzS0",
    client_secret="C93f_tmGEIprENWNiAgERJLr_vCJ3hFVi-7v65cdBDg3hNyVFvVWf6i1qlgMXQei",
    api_base_url="https://dev-jnz--huf.eu.auth0.com",
    access_token_url="https://dev-jnz--huf.eu.auth0.com/oauth/token",
    authorize_url="https://dev-jnz--huf.eu.auth0.com/authorize",
    client_kwargs={"scope": "openid profile email",},
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "profile" not in session:
            # Redirect to Login page here
            return redirect("/")
        return f(*args, **kwargs)

    return decorated
