from flask_mysql_connector import MySQL

def create_tables():
    mysql = MySQL()
    conn = mysql.connection
    cursor = conn.cursor()

    sql_script = """
    CREATE TABLE IF NOT EXISTS college (
        collegeCode VARCHAR(50) PRIMARY KEY,
        collegeName VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS course (
        courseCode VARCHAR(20) PRIMARY KEY,
        courseName VARCHAR(100) UNIQUE NOT NULL,
        collegeCode VARCHAR(50),
        FOREIGN KEY (collegeCode) REFERENCES college(collegeCode)
    );
    CREATE TABLE IF NOT EXISTS student (
        studentID VARCHAR(10) PRIMARY KEY,
        firstName VARCHAR(50) NOT NULL,
        lastName VARCHAR(50) NOT NULL,
        yearlevel VARCHAR(10) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        courseCode VARCHAR(20),
        FOREIGN KEY (courseCode) REFERENCES course(courseCode)
    );
    """
    
    cursor.execute(sql_script, multi=True)
    conn.commit()
    cursor.close()