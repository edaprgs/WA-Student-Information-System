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
    def delete(cls, courseCode):
        try:
            cursor = mysql.connection.cursor()

            # Check if the course is referenced in any student
            check_students_sql = f"SELECT COUNT(*) FROM student WHERE course = '{courseCode}'"
            cursor.execute(check_students_sql)
            num_students = cursor.fetchone()[0]

            if num_students > 0:
                # Course is referenced, show a prompt or message
                return "The course cannot be deleted since it is associated with students."

            # No students are associated, proceed with deletion
            delete_course_sql = f"DELETE FROM course WHERE courseCode = '{courseCode}'"
            cursor.execute(delete_course_sql)
            mysql.connection.commit()
            
            return True

        except:
            return False

    @classmethod
    def get_courses(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM course") 
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