from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class course_form(FlaskForm):
    courseCode = StringField('Course Code', validators=[DataRequired(), Length(min=4, max=20)])
    courseName = StringField('Course Name', validators=[DataRequired(), Length(min=10, max=100)])
    collegeCode = StringField('College Code', validators=[Length(max=50)])
    submit = SubmitField("Submit")