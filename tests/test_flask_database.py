from flask_testing import TestCase

from mabd import flask_interface
from mabd.flask_interface import db


class FlaskTests(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/blah.sqlite"

    def create_app(self):
        app = flask_interface.create_app()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_can_see_that_database_was_created(self):
        pass

    # def test_can_add_user_to_database():
    #     app = flask_interface.create_app()
    #     app.app_context().push()
