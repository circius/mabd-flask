from flask import Flask

import os


def create_app(test_config=None):
    app = Flask(
        "mabd.flask_interface",
        # root_path="~/projects/mabd_python_proper/src/mabd/flask_interface/",
        # template_folder="~/projects/mabd_python_proper/src/mabd/flask_interface/templates",
    )

    print(f"Root path for Flask: {app.root_path}")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import admin

    app.register_blueprint(admin.bp)
    app.add_url_rule("/", endpoint="")

    return app
