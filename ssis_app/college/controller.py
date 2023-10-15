from flask import render_template, redirect, request, jsonify
from . import college_bp
import ssis_app.models as models
from ssis_app.college.forms import UserForm


@college_bp.route('/college')
@college_bp.route('/')
def index():
    users = models.Users.all()
    return render_template('index.html', data=users,title='Home',something='something')

@college_bp.route('/user/register', methods=['POST','GET'])
def register():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = models.Users(email=form.email.data, password=form.password.data,username=form.username.data)
        user.add()
        return redirect('/')
    else:
        return render_template('signup.html', form=form)

@college_bp.route("/user/delete", methods=["POST"])
def delete():
    id = request.form['id']
    if models.Users.delete(id):
        return jsonify(success=True,message="Successfully deleted")
    else:
        return jsonify(success=False,message="Failed")          