from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class student_form(FlaskForm):
    student_ID = StringField('Student ID', validators=[DataRequired(), Length(max=10)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    course_code = StringField('Course', validators=[DataRequired(), Length(max=20)])
    selectedYLevel = StringField('Year Level', validators=[DataRequired(), Length(max=10)])
    selectedGender = StringField('Gender', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField("Submit")