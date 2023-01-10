from flask import request
from Models.Admin_16_12_22 import Admin
from Models.Student_6_12_22 import Students
from DbConnection_30_11_22 import db
from werkzeug.security import generate_password_hash

class Password:
    @staticmethod
    def Forgot_password():
        user_id= request.form.get('UserID')
        # print(user_id)
        admin_data = Admin.query.filter_by(ProfID=user_id).first()
        if admin_data:
            print("Your UserID is", admin_data.ProfID)
            return 'Your UserID is'+ admin_data.ProfID +'\nclick the link to change your password ' + 'http://127.0.0.1:600/change_pass/' + admin_data.ProfID
        else:
            student_data = Students.query.filter_by(UserID=user_id).first()
            if student_data:
                print("Your UserID is", student_data.UserID)
                return 'click the link to change your password' + 'http://127.0.0.1:600/change_pass/' + student_data.UserID
            else:
                return 'No such UserID found'

    @staticmethod
    def Change_password(user_id):
        password = request.form.get('Password')
        re_password = request.form.get('Re-enter password')
        admin_data = Admin.query.filter_by(ProfID=user_id).first()
        # print(password)
        if password == re_password:
            if admin_data:
                encpass = generate_password_hash(password)
                Admin.query.filter_by(ProfID=admin_data.ProfID).update({'Password': encpass})
                db.session.commit()
                return 'updated'
            else:
                student_data = Students.query.filter_by(UserID=user_id).first()
                if student_data:
                    encpass = generate_password_hash(password)
                    Students.query.filter_by(UserID=student_data.UserID).update({'Password': encpass})
                    db.session.commit()
                    return 'updated'
                else:
                    return 'No user found'
        else:
            return 'passwords are not matching'
