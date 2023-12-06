from flask import render_template, request
from ssis_app.course.forms import *
import ssis_app.models as models
from ssis_app.models.course import course
from flask import Blueprint

course_bp = Blueprint('course', __name__)

@course_bp.route('/add/', methods=['GET', 'POST'])
def add_course():
    form = course_form()
    new_course = course()
    college_codes = new_course.get_college_codes()
    if request.method == "POST":
        course_code = form.course_code.data.upper()
        course_name = form.course_name.data.upper()
        college_code = form.college_code.data

        new_course.courseCode = course_code 
        new_course.courseName = course_name     
        new_course.collegeCode = college_code
        
        result = new_course.add()

        if result:
            return render_template('add_course.html', success=True, course_form=form)
        else:
            return render_template('add_course.html', error=True, course_form=form)

    return render_template('add_course.html',course_form=form, college_codes=college_codes)

@course_bp.route('/edit/', methods=['GET', 'POST'])
def course_edit():
    form = course_form()
    update_course = course()
    college_codes = update_course.get_college_codes()
    if request.method == 'GET':
        course_code = request.args.get('course_code')
        course_name = request.args.get('course_name')   
        college_code = request.args.get('college_code') 
        return render_template('edit_course.html', college_codes=college_codes,code=course_code, name=course_name, college=college_code, course_form=form)
    elif request.method == 'POST':
        _course_code = form.course_code.data
        new_course_name = form.course_name.data.upper()
        new_college = form.college_code.data

        updated = course.update(courseCode=_course_code, courseName=new_course_name, collegeCode=new_college)  
        
        if updated:
            return render_template('edit_course.html', success=True, course_form=form)
        else:
            return render_template('edit_course.html', error=True, course_form=form)
        
    return render_template("edit_course.html", course_form=form)

@course_bp.route('/delete/', methods=['GET', 'POST'])
def course_delete():
    form = course_form()

    if request.method == "POST":
        code = form.course_code.data
        name = form.course_name.data
        college = form.college_code.data

        result = course.delete(code, name, college)
        print(result, code, name, college)

        if result:
            return render_template('course_list.html', success=True, course_form=form)
        else:
            return render_template('course_list.html', error=True, course_form=form)
            
    return render_template("course_list.html", course_form=form)

@course_bp.route('/list/')
def course_list():
    courses_data = course.get_courses()
    return render_template('course_list.html', courses=courses_data)

@course_bp.route('/search/', methods=['GET', 'POST'])
def search_courses():
    query = request.form.get('query')
    selected_field = request.form.get('selectedField')
    results = course.search(query, selected_field)

    return render_template('search_results.html', results=results, context="course")