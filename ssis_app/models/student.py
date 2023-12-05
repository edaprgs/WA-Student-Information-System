from ssis_app import mysql
import os

class student(object):

    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT studentID FROM student WHERE studentID = %s"
        cursor.execute(check_duplicate_sql, (self.studentID,))
        existing_student = cursor.fetchone()

        if existing_student:
            return False

        sql = "INSERT INTO student(studentID, firstName, lastName, course, yearlevel, gender, profilePhoto) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.studentID, self.firstName, self.lastName, self.course, self.yearlevel, self.gender, self.profilePhoto))
        mysql.connection.commit()

        return True
    
    @classmethod
    def update(cls, studentID, firstName, lastName, course, yearlevel, gender, profilePhoto):
        cursor = mysql.connection.cursor()

        sql = "UPDATE student SET firstName = %s, lastName = %s, course = %s, yearlevel = %s, gender = %s, profilePhoto = %s WHERE studentID = %s"
        cursor.execute(sql, (firstName, lastName, course, yearlevel, gender, profilePhoto, studentID))
        print(sql, firstName, lastName, course, yearlevel, gender, studentID, profilePhoto)
        mysql.connection.commit()

        return True

    @classmethod
    def delete(cls, studentID):
        cursor = mysql.connection.cursor()

        delete_sql = "DELETE FROM student WHERE studentID = %s"
        cursor.execute(delete_sql, (studentID,))
        mysql.connection.commit()
        
        return True

    @classmethod
    def get_student(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student.*, college.collegeName, course.collegeCode FROM student INNER JOIN course ON course.courseCode = student.course INNER JOIN college ON course.collegeCode = college.collegeCode ORDER BY student.lastName ASC") 
        students = cursor.fetchall()
        cursor.close()

        student_list = []
        for student in students:
            profile_photo = student[6] if student[6] else None
            profile_photo_filename = os.path.basename(profile_photo.decode('utf-8')) if profile_photo else None
            print('PROFILE PHOTO:', profile_photo_filename)

            student_dict = {
                'studentID': student[0],
                'firstName': student[1],
                'lastName': student[2],
                'course': student[3],
                'yearlevel': student[4],
                'gender': student[5],
                'profilePhoto': f"https://res.cloudinary.com/ds0ppkkkj/image/upload/student_profile/{profile_photo_filename}" if profile_photo_filename else None,
                'collegeName': student[7],
                'collegeCode': student[8]
            }
            student_list.append(student_dict)

        return student_list
    
    @classmethod
    def get_student_info(cls, student_id):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM student WHERE studentID = %s"
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        if student:
            profile_photo = student[6] if student[6] else None
            profile_photo_filename = os.path.basename(profile_photo.decode('utf-8')) if profile_photo else None

            student_dict = {
                'studentID': student[0],
                'firstName': student[1],
                'lastName': student[2],
                'course': student[3],
                'yearlevel': student[4],
                'gender': student[5],
                'profilePhoto': f"https://res.cloudinary.com/ds0ppkkkj/image/upload/student_profile/{profile_photo_filename}" if profile_photo_filename else None
            }
            return student_dict
        else:
            return None

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
        
        elif selected_field == "COLLEGE":
            sql = "SELECT course.collegeCode FROM student JOIN course ON student.course = course.courseCode WHERE course.collegeCode LIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        else:
           sql = """
                SELECT student.*, college.collegeName, course.collegeCode 
                FROM student 
                INNER JOIN course ON course.courseCode = student.course
                INNER JOIN college ON course.collegeCode = college.collegeCode
                WHERE student.studentID LIKE %s 
                OR student.firstName LIKE %s 
                OR student.lastName LIKE %s 
                OR student.course LIKE %s 
                OR student.yearlevel LIKE %s 
                OR student.gender LIKE %s
                OR college.collegeName LIKE %s
                OR course.collegeCode LIKE %s
            """
        search_query = f"%{query}%"
        cursor.execute(sql, (search_query, search_query, search_query, search_query, search_query, search_query, search_query, search_query))

        results = cursor.fetchall()

        student_list = []
        for result in results:
            profile_photo = result[6] if result[6] else None
            profile_photo_filename = os.path.basename(profile_photo.decode('utf-8')) if profile_photo else None

            student_dict = {
                'studentID': result[0],
                'firstName': result[1],
                'lastName': result[2],
                'collegeCode': result[8],
                'course': result[3],
                'yearlevel': result[4],
                'gender': result[5],
                'profilePhoto': f"https://res.cloudinary.com/ds0ppkkkj/image/upload/student_profile/{profile_photo_filename}" if profile_photo_filename else None
            }
            student_list.append(student_dict)

        return student_list
    
    # get the college code from the college table for the college dropdown
    def get_course_codes(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT courseCode FROM course")
        course_codes = [row[0] for row in cursor.fetchall()]
        return course_codes