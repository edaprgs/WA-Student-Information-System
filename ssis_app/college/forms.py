from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class college_form(FlaskForm):
    college_code = StringField('CODE', validators=[DataRequired()])
    college_name = StringField('NAME', validators=[DataRequired(), Length(min=3, max=20)])
    search_input = StringField('SEARCH', render_kw={'placeholder': 'SEARCH'})
    submit = SubmitField("SUBMIT")