from flask import render_template, redirect, request, url_for, flash
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
            success_message = "College added successfully! Please check the list for updates"
        else:
            error_message = "College already exists."

    return render_template("add_college.html", college_form=form, success_message=success_message, error_message=error_message)

@college_bp.route('/edit/', methods=['GET', 'POST'])
def college_edit():
    success_message = None
    error_message = None
    if request.method == 'GET':
        college_code = request.args.get('college_code')
        college_name = request.args.get('college_name')    
        return render_template('edit_college.html', code = college_code, name=college_name)
    elif request.method == 'POST':
        _college_code = request.form.get('college_code')
        new_college_name = request.form.get('college_name').upper()

        updated = college.update(collegeCode=_college_code, collegeName=new_college_name)  
        
        success_message = ""
        error_message = ""

        if updated:
            success_message = "College updated successfully! Please check the list for updates"
        else:
            error_message = "College already exists."
        
        return render_template("edit_college.html", success_message=success_message, error_message=error_message)

@college_bp.route('/delete/', methods=['GET', 'POST'])
def college_delete():
    form = college_form()

    if request.method == "POST":
        code = request.form.get("college_code")
        name = request.form.get("college_name")

        result = college.delete(code, name)

        if result:
            return redirect(url_for('college.college_confirmation'))
        else:
            return redirect(url_for('college.college_error'))
            
    return render_template("college_list.html", college_form=form)

@college_bp.route('/college_confirmation/')
def college_confirmation():
    return render_template('confirmation.html', context="college")

@college_bp.route('/college_error/')
def college_error():
    return render_template('error.html', context="college")

@college_bp.route('/list/')
def college_list():
    colleges_data = college.get_colleges()
    return render_template('college_list.html', colleges=colleges_data)

@college_bp.route('/search/', methods=['GET', 'POST'])
def search_colleges():

    query = request.form.get('query')
    results = college.search(query)

    if not results:
        return "NO RECORDS FOUND"

    return render_template('search_results.html', results=results, context="college")
