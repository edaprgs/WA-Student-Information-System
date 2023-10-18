from flask import render_template, redirect, request
#from ssis_app.student.forms import student_form
import ssis_app.models as models
from ssis_app.models.student import student
from flask import Blueprint

student_bp = Blueprint('student', __name__)

@student_bp.route("/")
def index():
    return render_template("student.html")

@student_bp.route('/add/')
def add_student():
    return render_template('add_student.html')

@student_bp.route('/edit/')
def student_edit():
    return render_template('edit_student.html')

@student_bp.route('/delete/')
def student_delete():
    return render_template('delete_student.html')

@student_bp.route('/list/')
def student_list():
    return render_template('student_list.html')