import json
from urllib.request import urlopen
from functools import wraps

from flask import request, jsonify, _request_ctx_stack
from jose import jwt

from auth0.v3.management import Auth0

from .. import utilities

## management api stuff

AUTH0_DOMAIN = utilities.get_env_var_checked('AUTH0_DOMAIN')
MGMT_API_TOKEN = utilities.get_env_var_checked('AUTH0_MGMT_API_TOKEN')

auth0 = Auth0(AUTH0_DOMAIN, MGMT_API_TOKEN)

