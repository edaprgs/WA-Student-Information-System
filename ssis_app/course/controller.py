from flask import render_template, redirect, request
#from ssis_app.course.forms import course_form
import ssis_app.models as models
from ssis_app.models.course import course
from flask import Blueprint

course_bp = Blueprint('course', __name__)

@course_bp.route("/")
def index():
    return render_template("course.html")

@course_bp.route('/add/')
def add_course():
    return render_template('add_course.html')

@course_bp.route('/edit/')
def course_edit():
    return render_template('edit_course.html')

@course_bp.route('/delete/')
def course_delete():
    return render_template('delete_course.html')

@course_bp.route('/list/')
def course_list():
    return render_template('course_list.html')