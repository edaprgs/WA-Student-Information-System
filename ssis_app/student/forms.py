from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class student_form(FlaskForm):
    studentID = StringField('Student ID', validators=[DataRequired(), Length(max=10)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    course = StringField('Course', validators=[DataRequired(), Length(max=20)])
    yearlevel = StringField('Year Level', validators=[DataRequired(), Length(max=10)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField("Submit")
    submit = SubmitField("Update")