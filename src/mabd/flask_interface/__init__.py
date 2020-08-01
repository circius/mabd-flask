import os, logging, sys

from flask import Flask

from . import extensions, auth0, config

from .. import utilities


def create_app():
    app = Flask("mabd.flask_interface")

    log = logging.getLogger('authlib')
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.DEBUG)

    extensions.oauth.init_app(app)

    flask_config = os.getenv("FLASK_CONFIG_OBJECT")
    if flask_config == "Development":
        print("running development")
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(config.Config)

    # if test_config is None:
    #     app.config.from_object(config.Config)
    # else:
    #     app.config.from_mapping(test_config)

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
