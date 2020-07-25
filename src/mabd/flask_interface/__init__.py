from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os


def create_app(test_config=None):
    app = Flask("mabd.flask_interface")

    if test_config is None:
        pass
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
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

    return app
