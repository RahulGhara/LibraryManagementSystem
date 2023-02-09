import re
import ssl
import uuid
from flask import request
from DbConnection_30_11_22 import db, app
from Models.Student_6_12_22 import Students
from JWT.LoginApi_16_12_22 import token_required
from werkzeug.security import generate_password_hash
import smtplib
from email.message import EmailMessage
import jwt
from logger_16_1_23 import logger


class StudentTableApi:
    @staticmethod
    @token_required
    def AddStudent(current_user):
        logger.debug('AddStudent api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            # breakpoint()
            logger.debug('This is in the authentication block now')
            if data['ProfID']:
                roll_no_pattern= r'^[A-Z]{3,4}[_][0-9]{4}[_][0-9]{4,5}$'
                pass_pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                phn_no_pattern= r'^[0-9]{10}$'
                student_id = uuid.uuid4()
                roll_no = request.form.get('RollNo')
                name = request.form.get('Name')
                department = request.form.get('Department')
                semester = request.form.get('Semester')
                passout_year = request.form.get('PassoutYear')
                user_id = 'STD_' + roll_no
                std_pass = request.form.get('Password')
                email = request.form.get('Email')
                phn_no = request.form.get('PhnNo')
                logger.debug('Checking roll_no pattern')
                if re.match(roll_no_pattern,roll_no):
                    logger.debug('Checking password pattern')
                    if re.match(pass_pattern,std_pass):
                        encpass = generate_password_hash(std_pass)
                        logger.debug('validating email')
                        if re.match(email_pattern,email):
                            logger.debug('checking phn_no')
                            if re.match(phn_no_pattern,phn_no):
                                new_entry = Students(student_id, roll_no, name, department, semester, passout_year, user_id, encpass, email,
                                                     phn_no)
                                db.session.add(new_entry)
                                db.session.commit()
                                logger.debug('New entry created')
                                token = request.headers['access_token']
                                data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')

                                '''sending email'''
                                if data['Email']:
                                    sender_email = data['Email']
                                    rec_email = email
                                    msg = EmailMessage()
                                    msg['Subject'] = 'Autogenerated ID and Password from Library'
                                    msg['From'] = 'Library admin'
                                    msg['to'] = email
                                    msg.set_content('Hello,' + name +
                                                    '\nYour user name is :' + user_id + 'and Password: ' + std_pass +
                                                    '\n This is an auto generated mail from library'
                                                    '\n Please do not reply.')
                                    context = ssl.create_default_context()
                                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                        smtp.login(sender_email, "qsbnvxdoikusyeyr")
                                        smtp.sendmail(rec_email, rec_email, msg.as_string())

                                    # smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
                                    # smtpObj.starttls()
                                    # smtpObj.login('rahul.ghara@bedev.cbnits.com', 'orjkzkkdvlfxqxaa')
                                    # message = 'you user name is :'
                                    # smtpObj.sendmail('rahul.ghara@bedev.cbnits.com', rec_email,msg=message)
                                    logger.debug('Mail sent successfully')
                                return 'entry successful'
                            else:
                                logger.error('Phn_no is not correct')
                                return 'Enter correct 10 digit Phn no.'
                        else:
                            logger.error('Email is not correct')
                            return 'Enter correct Email'
                    else:
                        logger.error('Password pattern is not correct')
                        return 'Password pattern is not correct'
                else:
                    logger.error('Roll_no is not in the correct format')
                    return 'Roll_no is not in the correct format'

        except:
            logger.error('user is not authorized')
            return 'You are not authorized to access this'
    @staticmethod
    @token_required
    def ViewStudentData(current_user, roll_no):
        logger.debug('ViewStudent api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            logger.debug('This is in the authentication block now')
            if data['ProfID']:
                student_data = Students.query.filter_by(RollNo=roll_no).first()
                if student_data:
                    data = [student_data.StudentID, student_data.RollNo, student_data.Name, student_data.Department,
                            student_data.Semester, student_data.PassoutYear]
                    return data
                else:
                    return 'No student found for this roll no'
        except:
            logger.error('Not authorized to access this')
            return 'You are not authorized to access this'

    @staticmethod
    @token_required
    def UpdateStudentData(current_user, roll_no):
        logger.debug('UpdateStudentData api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        phn_no_pattern = r'^[0-9]{10}$'
        changed_sem=request.form.get('Semester')
        new_mail=request.form.get('Email')
        new_phn_no= request.form.get('PhnNo')
        try:
            logger.debug('This is in the authentication block now')
            if data['ProfID']:
                student_data = Students.query.filter_by(RollNo=roll_no).first()
                if student_data:
                    if changed_sem == None and new_mail == None and new_phn_no == None:
                        logger.error('No fields given to update')
                        return "No fields are given to update"
                    if changed_sem =='' or new_mail== '' or new_phn_no == '':
                        logger.error('some of the given fields are empty')
                        return 'give values to all fields'
                    if changed_sem:
                        Students.query.filter_by(RollNo=roll_no).update({'Semester': changed_sem})
                        logger.info('Semester updated')
                    if new_mail:
                        if re.match(email_pattern,new_mail):
                            Students.query.filter_by(RollNo=roll_no).update({'Email': new_mail})
                            logger.info('Email updated')
                        else:
                            logger.error('new mail pattern is not matching')
                            return 'Enter valid email'
                    if new_phn_no:
                        if re.match(phn_no_pattern,new_phn_no):
                            Students.query.filter_by(RollNo=roll_no).update({'PhnNo': new_phn_no})
                            logger.info('PhnNo updated')
                        else:
                            logger.error('Phn no is not valid')
                            return 'Enter valid 10 digit PhnNo'
                    # student_data.Semester = request.form.get('Semester')
                    db.session.commit()
                    logger.debug('record updated')
                    return 'Updated'
                else:
                    logger.error('No student found for this rollno')
                    return 'No student found'
        except:
            logger.error('user is not authorized')
            return 'You are not authorized to access this'

    @staticmethod
    @token_required
    def DeleteStudent(current_user,roll_no):
        logger.debug('DeleteStudent api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            logger.debug('This is in the authentication block now')
            if data['ProfID']:
                student_data = Students.query.filter_by(RollNo=roll_no).first()
                if student_data:
                    db.session.delete(student_data)
                    db.session.commit()
                    logger.debug('record deleted')
                    return 'Student deleted from database'
                else:
                    logger.error('No student found for this rollno')
                    return 'Student record not found'
        except:
            logger.error('user is not authorized')
            return 'You rae not authorized to access this'
