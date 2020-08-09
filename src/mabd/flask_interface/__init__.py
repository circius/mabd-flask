import os, logging, sys

from flask import Flask

from . import extensions, auth0, config

from .. import utilities


def create_app():
    app = Flask("mabd.flask_interface")

    extensions.oauth.init_app(app)

    config_to_load = os.getenv("CONFIG_TO_LOAD")

    if config_to_load == "development":
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(config.Config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ## submodules

    from . import admin

    app.register_blueprint(admin.bp, url_prefix="/admin")

    from . import user

    app.register_blueprint(user.bp, url_prefix="/")

    return app
