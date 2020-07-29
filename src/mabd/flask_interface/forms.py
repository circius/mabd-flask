from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, StopValidation

from . import models

def username_exists_in_db_P(form, field):
    this_username = field.data
    print(this_username)
    user_exists = models.db.session.query(
        models.User.id).filter_by(
            username=this_username).first()
    if user_exists is None:
        print("no user exists")
        print(f"will now call {StopValidation}")
        raise StopValidation('User does not exist.')


class UserNameMustExist(object):
    def __init__(self):
        self.message = "User does not exist"
    def __call__(self, form, field):
        check = models.db.session.query(
            models.User.id).filter_by(username=field.data).first()
        print(check)
        if True:#check is None:
            print(f"running Stopvalidation {StopValidation}")
            raise StopValidation(self.message)


class PasswordMustBeCorrect(object):
    def __init__(self):
        self.message = "Incorrect password"
    def __call__(self, form, field):
        username = form.username.data
        password = field.data
        user = models.db.session.query(models.User.id).filter_by(username=form.username.data).one()

        if not user.check_password(password):
            raise ValidationError('Password is incorrect.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
