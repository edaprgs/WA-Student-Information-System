from ssis_app import mysql

class course(object):
    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT courseCode FROM course WHERE courseCode = %s"
        cursor.execute(check_duplicate_sql, (self.courseCode,))
        existing_course = cursor.fetchone()

        if existing_course:
            return False

        sql = "INSERT INTO course(courseCode, courseName, collegeCode) VALUES(%s, %s, %s)"
        cursor.execute(sql, (self.courseCode, self.courseName, self.collegeCode))
        mysql.connection.commit()

        return True
    
    @classmethod
    def update(cls, courseCode, courseName, collegeCode):
        cursor = mysql.connection.cursor()

        sql = "UPDATE course SET courseName = %s, collegeCode = %s WHERE courseCode = %s"
        cursor.execute(sql, (courseName, collegeCode, courseCode))
        print(sql, courseName, collegeCode, courseCode)
        mysql.connection.commit()

        return True

    @classmethod
    def delete(cls, courseCode, courseName, collegeCode):
        cursor = mysql.connection.cursor()

        check_association_sql = "SELECT studentID FROM student WHERE course = %s"
        cursor.execute(check_association_sql, (courseCode,))
        associated_student = cursor.fetchone()

        if associated_student:
            return False

        delete_sql = "DELETE FROM course WHERE courseCode = %s AND courseName = %s AND collegeCode = %s"
        cursor.execute(delete_sql, (courseCode, courseName, collegeCode))
        mysql.connection.commit()
        
        return True

    @classmethod
    def get_courses(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM course ORDER BY courseName") 
        courses = cursor.fetchall()
        cursor.close()
        return courses

    @classmethod
    def search(cls, query, selected_field):
        cursor = mysql.connection.cursor()
        if selected_field == "CODE":
            sql = "SELECT * FROM course WHERE courseCode LIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        elif selected_field == "NAME":
            sql = "SELECT * FROM course WHERE courseName LIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        elif selected_field == "COLLEGE":
            sql = "SELECT * FROM course WHERE collegeCode LIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        else:
            sql = "SELECT * FROM course WHERE courseCode LIKE %s OR courseName LIKE %s OR collegeCode LIKE %s"
            cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()

        return results

    def get_college_codes(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT collegeCode FROM college")
        college_codes = [row[0] for row in cursor.fetchall()]
        return college_codes