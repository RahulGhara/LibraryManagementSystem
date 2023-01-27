from flask import request
from Models.Admin_16_12_22 import Admin
from Models.Student_6_12_22 import Students
from DbConnection_30_11_22 import db
from werkzeug.security import generate_password_hash
import re
from logger_16_1_23 import logger


class Password:
    @staticmethod
    def Forgot_password():
        logger.debug('Forgot_Password api is running')
        user_id = request.form.get('UserID')
        # print(user_id)
        admin_data = Admin.query.filter_by(ProfID=user_id).first()
        if admin_data:
            logger.info(f'creating forgot password link for {admin_data.ProfID}')
            print("Your UserID is", admin_data.ProfID)
            return 'Your UserID is' + admin_data.ProfID + '\nclick the link to change your password ' + ' http://127.0.0.1:600/change_pass/' + admin_data.ProfID
        else:
            student_data = Students.query.filter_by(UserID=user_id).first()
            if student_data:
                logger.info(f'creating forgot password link for {student_data.UserID}')
                print("Your UserID is", student_data.UserID)
                return 'click the link to change your password' + 'http://127.0.0.1:600/change_pass/' + student_data.UserID
            else:
                logger.error('UserID is not valid')
                return 'No such UserID found'

    @staticmethod
    def Change_password(user_id):
        logger.debug('Change_Password api is running')
        password = request.form.get('Password')
        re_password = request.form.get('Re-enter password')
        admin_data = Admin.query.filter_by(ProfID=user_id).first()
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        # print(password)
        if password == re_password:
            logger.debug('password matched')
            if re.match(password_pattern, password):
                logger.debug('password type matched')
                if admin_data:
                    encpass = generate_password_hash(password)
                    Admin.query.filter_by(ProfID=admin_data.ProfID).update({'Password': encpass})
                    db.session.commit()
                    logger.debug('new password updated for admin')
                    return 'updated'
                else:
                    student_data = Students.query.filter_by(UserID=user_id).first()
                    if student_data:
                        encpass = generate_password_hash(password)
                        Students.query.filter_by(UserID=student_data.UserID).update({'Password': encpass})
                        db.session.commit()
                        logger.debug('new password updated for student')
                        return 'updated'
                    else:
                        logger.error('No user found')
                        return 'No user found'
            else:
                logger.error('password pattern not matched')
                return 'Password pattern is not matching'
        else:
            logger.error('passwords are not matching')
            return 'passwords are not matching'
