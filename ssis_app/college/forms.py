from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class college_form(FlaskForm):
    college_code = StringField('CODE', validators=[DataRequired(), Length(min=3, max=50)])
    college_name = StringField('NAME', validators=[DataRequired(), Length(min=10, max=100)])
    submit = SubmitField("SUBMIT")
    submit = SubmitField('Update')