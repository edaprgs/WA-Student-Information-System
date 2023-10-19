from flask import render_template, redirect, request, url_for
from ssis_app.course.forms import *
import ssis_app.models as models
from ssis_app.models.course import course
from flask import Blueprint

course_bp = Blueprint('course', __name__)

@course_bp.route("/")
def index():
    return render_template("course.html")

@course_bp.route('/add/', methods=['GET', 'POST'])
def add_course():
    form = course_form()
    new_course = course()
    college_codes = new_course.get_college_codes()
    success_message = None
    error_message = None

    if request.method == "POST":
        course_code = request.form.get("course_code").upper()
        course_name = request.form.get("course_name").upper()
        college_code = request.form.get("college_code")

        new_course.courseCode = course_code 
        new_course.courseName = course_name     
        new_course.collegeCode = college_code
        
        result = new_course.add()

        if result:
            success_message = "Course added successfully! Please check the list for updates"
        else:
            error_message = "Course already exists."

    return render_template('add_course.html',course_form=form, college_codes=college_codes, success_message=success_message, error_message=error_message)

@course_bp.route('/edit/', methods=['GET', 'POST'])
def course_edit():
    update_course = course()
    college_codes = update_course.get_college_codes()
    success_message = None
    error_message = None
    if request.method == 'GET':
        course_code = request.args.get('course_code')
        course_name = request.args.get('course_name')   
        college_code = request.args.get('college_code') 
        return render_template('edit_course.html', college_codes=college_codes,code=course_code, name=course_name, college=college_code)
    elif request.method == 'POST':
        _course_code = request.form.get('course_code')
        new_course_name = request.form.get('course_name').upper()
        new_college = request.form.get('college_code')

        updated = course.update(courseCode=_course_code, courseName=new_course_name, collegeCode=new_college)  
        
        success_message = ""
        error_message = ""

        if updated:
            success_message = "Course updated successfully! Please check the list for updates"
        else:
            error_message = "Course already exists."
        
        return render_template("edit_course.html", success_message=success_message, error_message=error_message)

@course_bp.route('/delete/', methods=['GET', 'POST'])
def course_delete():
    form = course_form()

    if request.method == "POST":
        code = request.form.get("course_code")
        name = request.form.get("course_name")
        college = request.form.get("college_code")

        result = course.delete(code, name, college)
        print(result, code, name, college)

        if result:
            return redirect(url_for('course.course_confirmation'))
        else:
            return redirect(url_for('course.course_error'))
            
    return render_template("course_list.html", college_form=form)

@course_bp.route('/course_confirmation/')
def course_confirmation():
    return render_template('confirmation.html', context="course")

@course_bp.route('/course_error/')
def course_error():
    return render_template('error.html', context="course")

@course_bp.route('/list/')
def course_list():
    courses_data = course.get_courses()
    return render_template('course_list.html', courses=courses_data)