import os


class Config(object):
    """ Base config
"""

    print("loading base config")
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    """ Config for development.
"""

    DEBUG = True
    TESTING = True
