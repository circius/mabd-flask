from werkzeug.middleware.proxy_fix import ProxyFix

from mabd import flask_interface

def app(errors, request):
    print(f"errors: {errors}")
    print(f"request: {request}")
    
    naive_app = flask_interface.create_app()
    app = ProxyFix(naive_app, x_for=1, x_proto=1)
    app.run(host='0.0.0.0')
