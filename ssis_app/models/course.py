from ssis_app import mysql

class course(object):

    def add(self):
        cursor = mysql.connection.cursor()

        sql = f"INSERT INTO users(username,user_password,email) \
                VALUES('{self.username}',md5('{self.password}'),'{self.email}')" 

        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from users"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls,id):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from users where id= {id}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False

        
