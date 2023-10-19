from ssis_app import mysql

class college(object):

    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT collegeCode FROM college WHERE collegeCode = %s"
        cursor.execute(check_duplicate_sql, (self.collegeCode,))
        existing_college = cursor.fetchone()

        if existing_college:
            return False

        sql = "INSERT INTO college(collegeCode, collegeName) VALUES(%s, %s)"
        cursor.execute(sql, (self.collegeCode, self.collegeName))
        mysql.connection.commit()

        return True

    @classmethod
    def update(cls, collegeCode, collegeName):
        cursor = mysql.connection.cursor()

        sql = "UPDATE college SET collegeName = %s WHERE collegeCode = %s"
        cursor.execute(sql, (collegeName, collegeCode))
        print(sql, collegeName, collegeCode)
        mysql.connection.commit()
        
        return True
    
    @classmethod
    def delete(cls, collegeCode):
        cursor = mysql.connection.cursor()

        check_courses_sql = f"SELECT COUNT(*) FROM course WHERE collegeCode = '{collegeCode}'"
        cursor.execute(check_courses_sql)
        num_courses = cursor.fetchone()[0]

        if num_courses > 0:
            return False

        delete_college_sql = f"DELETE FROM college WHERE collegeCode = '{collegeCode}'"
        cursor.execute(delete_college_sql)
        mysql.connection.commit()
        
        return True

    @staticmethod
    def get_colleges():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM college ORDER BY collegeName") 
        colleges = cursor.fetchall()
        cursor.close()
        return colleges
    
    @classmethod
    def search(cls, query):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM college WHERE collegeCode LIKE %s OR collegeName LIKE %s"
        cursor.execute(sql, (f"%{query}%", f"%{query}%"))
        result = cursor.fetchall()
        return result
    
    @classmethod
    def get_college_data(college_code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT collegeCode, collegeName FROM college WHERE collegeCode = ?", (college_code,))
        college_data = cursor.fetchone()
        return college_data