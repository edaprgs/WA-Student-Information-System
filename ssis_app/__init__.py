from flask import Flask, render_template
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect

mysql = MySQL()
bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
    )
    bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)

    @app.route("/home")
    def home():
        return render_template('home.html')

    @app.route("/student")
    def student():
        return render_template('student.html')

    @app.route("/college")
    def college():
        return render_template('college.html')

    @app.route("/course")
    def course():
        return render_template('course.html')

    @app.route("/add_college")
    def add_college():
        return render_template('add_college.html')

    @app.route("/add_course")
    def add_course():
        return render_template('add_course.html')

    return app