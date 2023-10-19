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
    
    # @classmethod
    # def update(cls, courseCode, courseName, collegeCode):
    #     cursor = mysql.connection.cursor()

    #     # Check if the new name is similar to any existing course names
    #     check_similarity_sql = "SELECT courseCode FROM course WHERE courseName = %s"
    #     cursor.execute(check_similarity_sql, (newCourseName,))
    #     similar_course = cursor.fetchone()

    #     if similar_course:
    #         # A similar course name exists, do not proceed with the update
    #         return "The new course name is too similar to an existing course."

    #     # If no similar course names are found, proceed with the update
    #     sql = "UPDATE course SET courseName = %s, collegeCode = %s WHERE courseCode = %s"
    #     cursor.execute(sql, (newCourseName, newCollegeCode, courseCode))
    #     mysql.connection.commit()

    #     return True

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
    def search(cls, query):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM course WHERE courseCode LIKE %s OR collegeName LIKE %s OR collegeCode LIKE %s"
        cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
        result = cursor.fetchall()
        return result
    
    # # get the college code from the college table for the college dropdown
    # @classmethod
    # def get_code(cls):
    #     cursor = mysql.connection.cursor()

    #     cursor.execute("SELECT collegeCode FROM college")
    #     college_codes = [row[0] for row in cursor.fetchall()]
    #     return college_codes

    def get_college_codes(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT collegeCode FROM college")
        college_codes = [row[0] for row in cursor.fetchall()]
        return college_codes