from .. import utilities


class Config(object):
    """ Base config
"""

    print("loading base config")
    DEBUG = False
    TESTING = False
    SECRET_KEY = utilities.get_env_var_checked("SECRET_KEY")


class DevelopmentConfig(Config):
    """ Config for development.
"""

    DEBUG = True
    TESTING = True
