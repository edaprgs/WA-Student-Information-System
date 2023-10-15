from ssis_app import mysql

class course(object):

    def add(self):
        cursor = mysql.connection.cursor()

        # Check if a course with the same courseCode already exists
        check_duplicate_sql = "SELECT courseCode FROM course WHERE courseCode = %s"
        cursor.execute(check_duplicate_sql, (self.courseCode,))
        existing_course = cursor.fetchone()

        # A course with the same courseCode already exists, do not proceed with the addition
        if existing_course:
            return "A course with the same courseCode already exists."

        # If no duplicate courseCode is found, proceed with the addition
        sql = "INSERT INTO course(courseCode, collegeName, collegeCode) VALUES(%s, %s, %s)"
        cursor.execute(sql, (self.courseCode, self.collegeName, self.collegeCode))
        mysql.connection.commit()

        return True
    
    @classmethod
    def update(cls, courseCode, newCourseName, newCollegeCode):
        cursor = mysql.connection.cursor()

        # Check if the new name is similar to any existing course names
        check_similarity_sql = "SELECT courseCode FROM course WHERE courseName = %s"
        cursor.execute(check_similarity_sql, (newCourseName,))
        similar_course = cursor.fetchone()

        if similar_course:
            # A similar course name exists, do not proceed with the update
            return "The new course name is too similar to an existing course."

        # If no similar course names are found, proceed with the update
        sql = "UPDATE course SET courseName = %s, collegeCode = %s WHERE courseCode = %s"
        cursor.execute(sql, (newCourseName, newCollegeCode, courseCode))
        mysql.connection.commit()

        return True

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
    def list(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM course"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def search(cls, query):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM course WHERE courseCode LIKE %s OR collegeName LIKE %s OR collegeCode LIKE %s"
        cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
        result = cursor.fetchall()
        return result