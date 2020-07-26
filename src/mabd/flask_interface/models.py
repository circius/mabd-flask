from flask import url_for

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManger
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    airtable_username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(128))
    administrator = db.Column(db.Boolean(), default=False)

    # self methods
    def __repr__(self):
        return "<User %r>" % self.username

    def __str__(self):
        return f"User {self.username}"

    # methods - getters

    def get_minimal_representation(self):
        return {
            "id": self.id,
            "username": self.username,
            "airtable_username": self.airtable_username,
            "administrator": self.administrator,
        }

    def get_login_link(self):
        return url_for('user.do_login', username=self.airtable_username)
        
    # methods - setters

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def set_username(self, string):
        self.username = string

    def set_airtable_username(self, string):
        self.airtable_username = string

    # methods

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
