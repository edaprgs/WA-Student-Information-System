from flask import render_template, redirect, request, jsonify
from ssis_app.college.forms import *
import ssis_app.models as models
from ssis_app.models.college import *
from flask import Blueprint

college_bp = Blueprint('college', __name__)

@college_bp.route("/")
def index():
    return render_template("college.html")

@college_bp.route('/add/', methods=["GET", "POST"])
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

@college_bp.route('/edit/')
def college_edit():
    return render_template('edit_college.html')

@college_bp.route('/delete/')
def college_delete():
    return render_template('delete_college.html')

@college_bp.route('/list/')
def college_list():
    colleges_data = college.get_colleges()
    return render_template('college_list.html', colleges=colleges_data)

@college_bp.route('/search/', methods=['POST'])
def college_search():
    query = request.form.get('search-input')
    colleges_data = college.search(query)
    return render_template('college_list.html', colleges=colleges_data)
