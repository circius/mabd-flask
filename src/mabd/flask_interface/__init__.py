from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from . import models

from .. import utilities

import os


def create_app(test_config=None):
    app = Flask("mabd.flask_interface")

    Bootstrap(app)

    models.login_manager.init_app(app)
    app.config['SECRET_KEY'] = utilities.get_env_var_checked("FLASK_WTF_SECRET_KEY")

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

    models.db.init_app(app)
    models.migrate.init_app(app, models.db)

    with app.app_context():
        models.db.create_all()

    ## add admin user if one doesn't already exist
    with app.app_context():
        admin_exists = models.db.session.query(
            models.db.session.query(models.User).filter_by(username='admin').exists()
        ).scalar()
        print(admin_exists)
        if not admin_exists:
            admin = models.User(username="admin", airtable_username=None, administrator=True)
            admin.set_password(utilities.get_env_var_checked("FLASK_ADMIN_PASSWORD"))
            models.db.session.add(admin)
            models.db.session.commit()
    ## submodules

    from . import admin

    app.register_blueprint(admin.bp, url_prefix="/admin")

    from . import user

    app.register_blueprint(user.bp, url_prefix="/")

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "User": models.User}

    return app
