from flask import render_template, redirect, request
from ssis_app.student.forms import *
import ssis_app.models as models
from ssis_app.models.student import *
from flask import Blueprint

student_bp = Blueprint('student', __name__)

@student_bp.route("/")
def index():
    return render_template("student.html")

@student_bp.route('/add/', methods=["GET", "POST"])
def add_student():
    form = student_form()
    new_student = student()
    course_codes = new_student.get_course_codes()
    success_message = None
    error_message = None

    if request.method == "POST":
        student_ID = request.form.get("student_ID").upper()
        first_name = request.form.get("first_name").upper()
        last_name = request.form.get("last_name").upper()
        course_code = request.form.get("course_code")
        year_level = request.form.get("selectedYLevel")
        gender = request.form.get("selectedGender")

        new_student.studentID = student_ID 
        new_student.firstName = first_name 
        new_student.lastName = last_name 
        new_student.course = course_code 
        new_student.yearlevel = year_level 
        new_student.gender = gender 
        result = new_student.add()

        if result:
            success_message = "Student added successfully!"
        else:
            error_message = "A student already exists."

    return render_template('add_student.html', course_codes=course_codes,student_form=form, success_message=success_message, error_message=error_message)

@student_bp.route('/edit/')
def student_edit():
    return render_template('edit_student.html')

@student_bp.route('/delete/')
def student_delete():
    return render_template('delete_student.html')

@student_bp.route('/list/')
def student_list():
    students_data = student.get_student()
    return render_template('student_list.html', students=students_data)