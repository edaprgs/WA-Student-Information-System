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
    def delete(cls, collegeCode, collegeName):
        cursor = mysql.connection.cursor()

        check_association_sql = "SELECT courseCode FROM course WHERE collegeCode = %s"
        cursor.execute(check_association_sql, (collegeCode,))
        associated_course = cursor.fetchone()

        if associated_course:
            return False

        delete_sql = "DELETE FROM college WHERE collegeCode = %s AND collegeName = %s"
        cursor.execute(delete_sql, (collegeCode, collegeName))
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
    def search(cls, query, selected_field):
        cursor = mysql.connection.cursor()
        if selected_field == "CODE":
            sql = "SELECT * FROM college WHERE collegeCode LIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        elif selected_field == "NAME":
            cursor.execute(sql, (f"%{query}%",))
            
        else:
            sql = "SELECT * FROM college WHERE collegeCode LIKE %s OR collegeName LIKE %s"
            cursor.execute(sql, (f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()

        return results
    
    @classmethod
    def get_college_data(college_code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT collegeCode, collegeName FROM college WHERE collegeCode = ?", (college_code,))
        college_data = cursor.fetchone()
        return college_data