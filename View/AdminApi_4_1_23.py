from Models.Admin_16_12_22 import Admin
from flask import request
from werkzeug.security import generate_password_hash
from DbConnection_30_11_22 import app, db
from JWT.LoginApi_16_12_22 import token_required
import smtplib
from email.message import EmailMessage
import jwt
import uuid
import ssl
import re
from logger_16_1_23 import logger


class AdminApi:
    @token_required
    @staticmethod
    def add_admin(current_user):
        logger.debug('add_admin api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        logger.debug('entering in the authentication block')
        try:
            if data.get('ProfID'):
                password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
                id_pattern = r"^[A-Z]{3,4}[_][0-9]{3,6}$"
                email_pattern= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                ID = uuid.uuid4()
                Name = request.form.get('Name')
                ProfID = request.form.get('ProfID')
                admin_pass = request.form.get('Password')
                # enc_pass = generate_password_hash(admin_pass)
                Designation = request.form.get('Designation')
                Email = request.form.get('Email')
                PhnNo = request.form.get('PhnNo')
                logger.debug('matching the ID pattern')
                if re.match(id_pattern, ProfID):
                    logger.debug('validating email')
                    if re.match(email_pattern,Email):
                        logger.debug('matching the password pattern')
                        if re.match(password_pattern, admin_pass):
                            enc_pass = generate_password_hash(admin_pass)
                            new_entry = Admin(ID, Name, ProfID, enc_pass, Designation, Email, PhnNo)
                            db.session.add(new_entry)
                            db.session.commit()
                            logger.debug('New entry successful')
                            # return 'entry successful'
                            if data['Email']:
                                sender_email = data['Email']
                                rec_email = Email
                                msg = EmailMessage()
                                msg['Subject'] = 'ID and autogenerated  Password from Library'
                                msg['From'] = 'Library admin'
                                msg['to'] = Email
                                msg.set_content('Hello,' + Name +
                                                '\nYour user name is :' + ProfID + 'and Password: ' + admin_pass +
                                                '\n This is an auto generated mail from library\n Please do not reply.')
                                context = ssl.create_default_context()
                                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    logger.warning('Logging in with email id and password')
                                    smtp.login(sender_email, "qsbnvxdoikusyeyr")
                                    smtp.sendmail(sender_email, rec_email, msg.as_string())
                                    logger.debug('mail sent')
                                return 'Mail Successfully send'
                        else:
                            logger.error('authentication error')
                            return "Password property not matched!"
                    else:
                        logger.error('Email does not exist')
                        return 'Enter correct Email'
                else:
                    logger.error("Prof_id pattern not matched")
                    return "Prof_id pattern is not correct"
        except:
            logger.error('user is not authorized')
            return 'You are not authorized to access this'

    @token_required
    @staticmethod
    def delete_admin(current_user, prof_id):
        logger.debug('delete_admin api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        logger.debug('entering the authentication block')
        try:
            if data['ProfID']:
                admin_data = Admin.query.filter_by(ProfID=prof_id).first()
                if admin_data:
                    db.session.delete(admin_data)
                    db.session.commit()
                    return 'Admin deleted from database'
                else:
                    return 'Admin does not found'
        except:
            logger.error('user is not authorized')
            return 'You are not authorized to access this'

    @token_required
    @staticmethod
    def update_admin(current_user, prof_id):
        logger.debug('update_admin api is running')
        designation = request.form.get('Designation')
        email = request.form.get('Email')
        PhnNo = request.form.get('PhnNo')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        logger.debug('entering the authentication block')
        try:
            if data['ProfID']:
                if designation is None and email is None and PhnNo is None:
                    return 'No fields given'
                elif designation == '' or email == '' or PhnNo == '':
                    return 'Give values to all specified fields'
                else:
                    if designation:
                        logger.debug('updating designation')
                        Admin.query.filter_by(ProfID=prof_id).update({'Designation': designation})
                    if email:
                        logger.debug('updating email')
                        Admin.query.filter_by(ProfID=prof_id).update({'Email': email})
                    if PhnNo:
                        logger.debug('updating PhnNo')
                        Admin.query.filter_by(ProfID=prof_id).update({'PhnNo': PhnNo})
                    db.session.commit()
                    return 'Updated'
        except:
            logger.error('user is not authorized')
            return 'You are not authorized to access this'
