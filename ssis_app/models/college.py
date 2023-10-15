from ssis_app import mysql

class college(object):

    def add(self):
        cursor = mysql.connection.cursor()

        sql = f"INSERT INTO college(collegeCode,collegeName) 
                VALUES('{self.collegeCode}',md5('{self.collegeName}'))" 

        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def update(cls, collegeCode, newCollegeName):
        cursor = mysql.connection.cursor()

        # Use placeholders to avoid SQL injection
        sql = "UPDATE college SET collegeName = %s WHERE collegeCode = %s"
        cursor.execute(sql, (newCollegeName, collegeCode))
        mysql.connection.commit()
    
    @classmethod
    def delete(cls,collegeCode):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from college where collegeCode= {collegeCode}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False

    @classmethod
    def list(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from college"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def search(cls, query):
        cursor = mysql.connection.cursor()

        # Use placeholders to avoid SQL injection
        sql = "SELECT * FROM college WHERE collegeCode LIKE %s OR collegeName LIKE %s"
        cursor.execute(sql, (f"%{query}%", f"%{query}%"))
        result = cursor.fetchall()
        return result