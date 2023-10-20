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
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student ORDER BY lastName") 
        students = cursor.fetchall()
        cursor.close()
        return students
    
    @classmethod
    def search(cls, query):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM student WHERE studentID LIKE %s OR firstName LIKE %s OR lastName LIKE %s OR course LIKE %s OR yearlevel LIKE %s OR gender LIKE %s"
        
        cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        result = cursor.fetchall()
        return result
    
    # get the college code from the college table for the college dropdown
    def get_course_codes(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT courseCode FROM course")
        course_codes = [row[0] for row in cursor.fetchall()]
        return course_codes