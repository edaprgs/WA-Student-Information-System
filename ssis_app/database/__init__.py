from flask import Flask
from flask_mysql_connector import MySQL
from .create_tables import create_tables

app = Flask(__name__)

# Configuration for MySQL connection
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "paragoso1234!"
app.config['MYSQL_DB'] = "ssis"

mysql = MySQL(app)

# Import and call the create_tables function to create the database tables
create_tables()