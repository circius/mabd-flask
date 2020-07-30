from flask import Flask

from . import extensions

from .. import utilities

import os


def create_app(test_config=None):
    app = Flask("mabd.flask_interface")

    extensions.oauth.init_app(app)

    app.config["SECRET_KEY"] = utilities.get_env_var_checked("FLASK_WTF_SECRET_KEY")
    if test_config is None:
        pass
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
