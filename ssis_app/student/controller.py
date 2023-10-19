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

@student_bp.route('/edit/', methods=['GET', 'POST'])
def student_edit():
    update_student = student()
    course_codes = update_student.get_course_codes()
    success_message = None
    error_message = None
    if request.method == 'GET':
        studentID = request.args.get('studentID')
        first_name = request.args.get('first_name')   
        last_name = request.args.get('last_name')   
        course_code = request.args.get('course_code')   
        year_level = request.args.get('year_level')   
        gender = request.args.get('gender')   
        print(studentID, first_name, last_name, course_code, year_level, gender)
        return render_template('edit_student.html', course_codes=course_codes,id=studentID, fname=first_name, lname=last_name, course=course_code, ylevel=year_level, sex=gender)
    elif request.method == 'POST':
        _studentID = request.form.get('studentID')
        new_fname = request.form.get('first_name').upper()
        new_lname = request.form.get('last_name').upper()
        new_course = request.form.get('course_code')
        new_ylevel = request.form.get('year_level')
        new_gender = request.form.get('gender')

        updated = student.update(studentID=_studentID, firstName=new_fname, lastName=new_lname, course=new_course, yearlevel=new_ylevel, gender=new_gender)  
        
        success_message = ""
        error_message = ""

        if updated:
            success_message = "Student information updated successfully! Please check the list for updates"
        else:
            error_message = "Student already exists."
        
        return render_template("edit_student.html", success_message=success_message, error_message=error_message)

@student_bp.route('/delete/')
def student_delete():
    return render_template('delete_student.html')

@student_bp.route('/list/')
def student_list():
    students_data = student.get_student()
    return render_template('student_list.html', students=students_data)