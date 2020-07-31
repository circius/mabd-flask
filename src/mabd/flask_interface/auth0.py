import json, os
from urllib.request import urlopen
from functools import wraps

from flask import request, jsonify, _request_ctx_stack
from jose import jwt

from auth0.v3.management import Auth0

## management api stuff

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
MGMT_API_TOKEN = os.getenv("AUTH0_MGMT_API_TOKEN")

auth0 = Auth0(AUTH0_DOMAIN, MGMT_API_TOKEN)
