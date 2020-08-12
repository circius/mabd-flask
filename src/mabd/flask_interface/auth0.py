import json, os
from urllib.request import urlopen
from functools import wraps

from flask import request, jsonify, _request_ctx_stack, current_app
from jose import jwt

from auth0.v3.management import Auth0
from auth0.v3.authentication import GetToken

## management api stuff

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_MGMT_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_MGMT_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

get_token = GetToken(AUTH0_DOMAIN)
token = get_token.client_credentials(
    AUTH0_MGMT_CLIENT_ID, AUTH0_MGMT_CLIENT_SECRET, f"https://{AUTH0_DOMAIN}/api/v2/"
)

mgmt_api_token = token["access_token"]

auth0 = Auth0(AUTH0_DOMAIN, mgmt_api_token)
