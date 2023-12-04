from flask import render_template, request, Blueprint, current_app
from ssis_app.student.forms import *
import ssis_app.models as models
from ssis_app.models.student import *
from flask import Blueprint
import os

student_bp = Blueprint('student', __name__)

@student_bp.route('/add/', methods=["GET", "POST"])
def add_student():
    form = student_form()
    new_student = student()
    course_codes = new_student.get_course_codes()
    if request.method == "POST":
        student_ID = request.form.get("student_ID").upper()
        first_name = request.form.get("first_name").upper()
        last_name = request.form.get("last_name").upper()
        course_code = request.form.get("course_code")
        year_level = request.form.get("selectedYLevel")
        gender = request.form.get("selectedGender")
        file_path = None
        current_app.config['UPLOAD_FOLDER'] = os.path.join(current_app.root_path, 'static', 'images')
        
        if 'input-file' in request.files:
            profile = request.files['input-file']
            if profile.filename != '':
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], profile.filename)
                profile.save(file_path)

        new_student.studentID = student_ID 
        new_student.firstName = first_name 
        new_student.lastName = last_name 
        new_student.course = course_code 
        new_student.yearlevel = year_level 
        new_student.gender = gender 
        new_student.profilePhoto = file_path
        print(file_path)
        result = new_student.add()

        if result:
            return render_template('add_student.html', success=True, student_form=form)
        else:
            return render_template('add_student.html', error=True, student_form=form)

    return render_template('add_student.html', course_codes=course_codes,student_form=form)

@student_bp.route('/edit/', methods=['GET', 'POST'])
def student_edit():
    update_student = student()
    course_codes = update_student.get_course_codes()
    if request.method == 'GET':
        studentID = request.args.get('studentID')
        student_info  = student.get_student_info(studentID)
        print("student info:", student_info)
        return render_template('edit_student.html', course_codes=course_codes, student=student_info)
   
    elif request.method == 'POST':
        _studentID = request.form.get('studentID')
        new_fname = request.form.get('first_name').upper()
        new_lname = request.form.get('last_name').upper()
        new_course = request.form.get('course_code')
        new_ylevel = request.form.get('year_level')
        new_gender = request.form.get('gender')
        file_path = None

        current_app.config['UPLOAD_FOLDER'] = os.path.join(current_app.root_path, 'static', 'images')
        
        if 'input-file' in request.files:
                profile = request.files['input-file']
                if profile.filename != '':
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], profile.filename)
                    profile.save(file_path)
                    print('File saved at:', file_path)  
        else:
            file_path = None

        print('New path:', file_path)

        student_info = student.get_student_info(_studentID)
        current_image_path = student_info['profilePhoto'] if student_info and 'profilePhoto' in student_info else None

        print('Old path:', current_image_path)

        if file_path:
            updated = student.update(studentID=_studentID, firstName=new_fname, lastName=new_lname, course=new_course, yearlevel=new_ylevel, gender=new_gender, profilePhoto=file_path)
        else:
            updated = student.update(studentID=_studentID, firstName=new_fname, lastName=new_lname, course=new_course, yearlevel=new_ylevel, gender=new_gender, profilePhoto=current_image_path)
        
        if updated:
            student_info = student.get_student_info(_studentID)
            return render_template('edit_student.html', success=True, student=student_info)
        else:
            return render_template('edit_student.html', error=True, student=student_info)
        
    return render_template("edit_student.html")

@student_bp.route('/delete/', methods=['POST'])
def student_delete():
    form = student_form()
    delete_student = student()

    if request.method == "POST":
        studentID = request.form.get('studentID')
        print('student id', studentID)

        result = delete_student.delete(studentID)

        if result:
            return render_template('student_list.html', success=True, student_form=form)
        else:
            return render_template('student_list.html', error=True, student_form=form)
            
    return render_template("student_list.html", student_form=form)

@student_bp.route('/list/')
def student_list():
    students_data = student.get_student()
    return render_template('student_list.html', students=students_data)

@student_bp.route('/search/', methods=['GET', 'POST'])
def search_students():
    query = request.form.get('query')
    selected_field = request.form.get('selectedField')
    results = student.search(query, selected_field)

    return render_template('search_results.html', results=results, context="student")
