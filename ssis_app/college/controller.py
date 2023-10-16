from flask import render_template, redirect, request
from ssis_app.college.forms import college_form
import ssis_app.models as models
from ssis_app.models.college import college
from flask import Blueprint

college_bp = Blueprint('college', __name__)

@college_bp.route('/add_college/', methods=["GET", "POST"])
def add_college():
    form = college_form()
    success_message = None
    error_message = None

    if request.method == "POST":
        code = request.form.get("college_code").upper()
        name = request.form.get("college_name").upper()

        new_college = college()
        new_college.collegeCode = code
        new_college.collegeName = name
        result = new_college.add()

        if result:
            success_message = "College added successfully!"
        else:
            error_message = "A college already exists."

    return render_template("add_college.html", college_form=form, success_message=success_message, error_message=error_message)
