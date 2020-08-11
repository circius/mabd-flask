# from werkzeug.middleware.proxy_fix import ProxyFix

from mabd import flask_interface


def application(errors, request):
    print(f"errors: {errors}")
    print(f"request: {request}")

    return flask_interface.create_app()
