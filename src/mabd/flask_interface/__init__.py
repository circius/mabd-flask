from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

import os


def create_app(test_config=None):
    app = Flask("mabd.flask_interface")

    Bootstrap(app)

    if test_config is None:
        pass
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from .models import db
    from .models import migrate

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    ## submodules

    from . import admin

    app.register_blueprint(admin.bp, url_prefix="/admin")

    from . import user

    app.register_blueprint(user.bp, url_prefix="/")

    # shell_context
    from . import models

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "User": models.User}

    return app
