from mabd import flask_interface

def cli():
    app = flask_interface.create_app()
    app.run(host='0.0.0.0')
