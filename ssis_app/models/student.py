from ssis_app import mysql

class student(object):

    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT studentID FROM student WHERE studentID = %s"
        cursor.execute(check_duplicate_sql, (self.studentID,))
        existing_student = cursor.fetchone()

        if existing_student:
            return False

        sql = "INSERT INTO student(studentID, firstName, lastName, course, yearlevel, gender) VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.studentID, self.firstName, self.lastName, self.course, self.yearlevel, self.gender))
        mysql.connection.commit()

        return True
    
    @classmethod
    def update(cls, studentID, firstName, lastName, course, yearlevel, gender):
        cursor = mysql.connection.cursor()

        sql = "UPDATE student SET firstName = %s, lastName = %s, course = %s, yearlevel = %s, gender = %s WHERE studentID = %s"
        cursor.execute(sql, (firstName, lastName, course, yearlevel, gender, studentID))
        print(sql, firstName, lastName, course, yearlevel, gender, studentID)
        mysql.connection.commit()

        return True

    @classmethod
    def delete(cls, studentID, firstName, lastName, course, yearlevel, gender):
        cursor = mysql.connection.cursor()

        delete_sql = "DELETE FROM student WHERE studentID = %s AND firstName = %s AND lastName = %s AND course = %s AND yearlevel = %s AND gender = %s"
        cursor.execute(delete_sql, (studentID, firstName, lastName, course, yearlevel, gender))
        mysql.connection.commit()
        
        return True

    @classmethod
    def get_student(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student.*, course.collegeCode FROM student JOIN course ON student.course = course.courseCode") 
        students = cursor.fetchall()
        cursor.close()
        return students
    
    @classmethod
    def search(cls, query, selected_field):
        cursor = mysql.connection.cursor()
        if selected_field == "STUDENT ID":
            sql = "SELECT * FROM student WHERE studentID LIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        elif selected_field == "FIRST NAME":
            sql = "SELECT * FROM student WHERE firstName LIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        elif selected_field == "LAST NAME":
            sql = "SELECT * FROM student WHERE lastName LIKE %s"
            cursor.execute(sql, (f"%{query}%",))
        
        elif selected_field == "COURSE":
            sql = "SELECT * FROM student WHERE course LIKE %s"
            cursor.execute(sql, (f"%{query}%",))
        
        elif selected_field == "YEAR LEVEL":
            sql = "SELECT * FROM student WHERE yearlevel LIKE %s"
            cursor.execute(sql, (f"%{query}%",))
        
        elif selected_field == "GENDER":
            if query.upper() == "FEMALE":
                sql = "SELECT * FROM student WHERE gender = 'FEMALE'"

            elif query.upper() == "MALE":
                sql = "SELECT * FROM student WHERE gender = 'MALE'"

            else:
                sql = "SELECT * FROM student"

            cursor.execute(sql, (f"%{query}%",))

        else:
           sql = """
                SELECT student.*, course.collegeCode 
                FROM student 
                JOIN course ON student.course = course.courseCode 
                WHERE student.studentID LIKE %s 
                OR student.firstName LIKE %s 
                OR student.lastName LIKE %s 
                OR student.course LIKE %s 
                OR student.yearlevel LIKE %s 
                OR student.gender LIKE %s
                OR course.collegeCode LIKE %s
            """
        search_query = f"%{query}%"
        cursor.execute(sql, (search_query, search_query, search_query, search_query, search_query, search_query, search_query))

        results = cursor.fetchall()

        return results
    
    # get the college code from the college table for the college dropdown
    def get_course_codes(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT courseCode FROM course")
        course_codes = [row[0] for row in cursor.fetchall()]
        return course_codes