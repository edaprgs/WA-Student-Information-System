from ssis_app import mysql

class student(object):

    def add(self):
        cursor = mysql.connection.cursor()

        # Check if a student with the same studentID already exists
        check_duplicate_sql = "SELECT studentID FROM student WHERE studentID = %s"
        cursor.execute(check_duplicate_sql, (self.studentID,))
        existing_student = cursor.fetchone()

        if existing_student:
            # A student with the same studentID already exists, do not proceed with the addition
            return "A student with the same studentID already exists."

        # If no duplicate studentID is found, proceed with the addition
        sql = "INSERT INTO student(studentID, firstName, lastName, course, yearlevel, gender) VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.studentID, self.firstName, self.lastName, self.course, self.yearlevel, self.gender))
        mysql.connection.commit()

        return True
    
    def update(self):
        cursor = mysql.connection.cursor()

        sql = f"UPDATE student SET firstName = '{self.firstName}', lastName = '{self.lastName}', \
                course = '{self.course}', yearlevel = '{self.yearlevel}', gender = '{self.gender}' \
                WHERE studentID = '{self.studentID}'"

        cursor.execute(sql)
        mysql.connection.commit()
    
    @classmethod
    def delete(cls,studentID):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE FROM student where studentID= {studentID}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False

    @classmethod
    def get_student(cls):
        cursor = mysql.connection.cursor()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student") 
        students = cursor.fetchall()
        cursor.close()
        return students
    
    @classmethod
    def search(cls, query):
        cursor = mysql.connection.cursor()

        sql = "SELECT studentID, firstName, lastName, course, yearlevel, gender FROM student \
                WHERE studentID LIKE %s OR firstName LIKE %s OR lastName LIKE %s \
                OR course LIKE %s OR yearlevel LIKE %s OR gender LIKE %s"
        
        cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        result = cursor.fetchall()
        return result
    
    # get the college code from the college table for the college dropdown
    def get_course_codes(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT courseCode FROM course")
        course_codes = [row[0] for row in cursor.fetchall()]
        return course_codes