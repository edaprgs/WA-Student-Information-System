from ssis_app import mysql

class college(object):

    def add(self):
        cursor = mysql.connection.cursor()

        # Check if a college with the same collegeCode already exists
        check_duplicate_sql = "SELECT collegeCode FROM college WHERE collegeCode = %s"
        cursor.execute(check_duplicate_sql, (self.collegeCode,))
        existing_college = cursor.fetchone()

        # A college with the same collegeCode already exists, do not proceed with the addition
        if existing_college:
            return "A college with the same collegeCode already exists."

        # If no duplicate collegeCode is found, proceed with the addition
        sql = "INSERT INTO college(collegeCode, collegeName) VALUES(%s, %s)"
        cursor.execute(sql, (self.collegeCode, self.collegeName))
        mysql.connection.commit()

        return True

    @classmethod
    def update(cls, collegeCode, newCollegeName):
        cursor = mysql.connection.cursor()

        # Check if the new name is similar to any existing college names
        check_similarity_sql = "SELECT collegeCode FROM college WHERE collegeName = %s"
        cursor.execute(check_similarity_sql, (newCollegeName,))
        similar_college = cursor.fetchone()

        # A similar college name exists, do not proceed with the update
        if similar_college:
            return "The new college name is too similar to an existing college."

        # If no similar college names are found, proceed with the update
        sql = "UPDATE college SET collegeName = %s WHERE collegeCode = %s"
        cursor.execute(sql, (newCollegeName, collegeCode))
        mysql.connection.commit()
        
        return True
    
    @classmethod
    def delete(cls, collegeCode):
        try:
            cursor = mysql.connection.cursor()

            # Check if the college is referenced in any course
            check_courses_sql = f"SELECT COUNT(*) FROM course WHERE collegeCode = '{collegeCode}'"
            cursor.execute(check_courses_sql)
            num_courses = cursor.fetchone()[0]

            if num_courses > 0:
                # College is referenced, show a prompt or message
                return "The college cannot be deleted since it is associated with courses."

            # No courses are associated, proceed with deletion
            delete_college_sql = f"DELETE FROM college WHERE collegeCode = '{collegeCode}'"
            cursor.execute(delete_college_sql)
            mysql.connection.commit()
            
            return True

        except:
            return False

    @classmethod
    def list(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM college"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def search(cls, query):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM college WHERE collegeCode LIKE %s OR collegeName LIKE %s"
        cursor.execute(sql, (f"%{query}%", f"%{query}%"))
        result = cursor.fetchall()
        return result