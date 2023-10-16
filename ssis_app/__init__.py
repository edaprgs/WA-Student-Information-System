from flask import Flask, render_template
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect
from ssis_app.college.forms import college_form

mysql = MySQL()
#bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
    )
    #bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)
  
    @app.route("/")
    def home():
        return render_template('home.html')
    
    @app.route('/college/')
    def college():
        return render_template('college.html')

    @app.route('/course/')
    def course():
        return render_template('course.html')   

    @app.route('/student/')
    def student():
        return render_template('student.html')
    
    @app.route('/add_college/')
    def add_college():
        form = college_form()
        return render_template('add_college.html', college_form=form)
    
    @app.route('/add_course/')
    def add_course():
        return render_template('add_course.html')

    @app.route('/add_student/')
    def add_student():
        return render_template('add_student.html')
    
    @app.route('/college_list/')
    def college_list():
        return render_template('college_list.html')
    
    @app.route('/course_list/')
    def course_list():
        return render_template('course_list.html')
    
    @app.route('/student_list/')
    def student_list():
        return render_template('student_list.html')
    
    
    #from ssis_app.routes.main_bp import main_bp
    from ssis_app.college.controller import college_bp
    #from ssis_app.routes.course_bp import course_bp
    #from ssis_app.routes.student_bp import student_bp
    
    #app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(college_bp, url_prefix='/college/')
    #app.register_blueprint(course_bp, url_prefix='/course/')
    #app.register_blueprint(student_bp, url_prefix='/student/')
   
    return app