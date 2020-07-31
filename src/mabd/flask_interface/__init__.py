import os

from flask import Flask

from . import extensions, auth0, config

from .. import utilities


def create_app(test_config=None):
    app = Flask("mabd.flask_interface")

    extensions.oauth.init_app(app)

    if test_config is None:
        app.config.from_object(config.Config)
    else:
        app.config.from_mapping(test_config)

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
