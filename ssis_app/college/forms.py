from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField


class UserForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=20)])
    email = StringField('Email Address', [validators.Length(min=10, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField("Submit")
