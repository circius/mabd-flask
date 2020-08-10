import os


class Config(object):
    """ Base config
"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    # authlib auth0 client settings
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_API_BASE_URL = "https://" + os.getenv("AUTH0_DOMAIN")
    AUTH0_ACCESS_TOKEN_URL = AUTH0_API_BASE_URL + "/oauth/token"
    AUTH0_AUTHORIZE_URL = "https://dev-jnz--huf.eu.auth0.com/authorize"
    AUTH0_CLIENT_KWARGS = {"scope": "openid profile email"}


class DevelopmentConfig(Config):
    """ Config for development.
"""

    DEBUG = True
    TESTING = True
