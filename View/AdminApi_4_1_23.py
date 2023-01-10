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


class AdminApi:
    # @token_required
    @staticmethod
    def add_admin():

        token = request.headers['access_token']
        data= jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            if data['ProfID']:
                ID = uuid.uuid4()
                Name = request.form.get('Name')
                ProfID = request.form.get('ProfID')
                admin_pass = request.form.get('Password')
                enc_pass = generate_password_hash(admin_pass)
                Designation = request.form.get('Designation')
                Email = request.form.get('Email')
                PhnNo = request.form.get('PhnNo')

                new_entry = Admin(ID, Name, ProfID, enc_pass, Designation, Email, PhnNo)
                db.session.add(new_entry)
                db.session.commit()
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
                        smtp.login(sender_email, "qsbnvxdoikusyeyr")
                        smtp.sendmail(sender_email, rec_email, msg.as_string())
                    return 'Mail Successfully send'
        except:
            return 'You are not authorized to access this'

    @token_required
    @staticmethod
    def delete_admin(current_user, prof_id):
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
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
            return 'You are not authorized to access this'

    # @token_required
    # @staticmethod
    # def update_admin(current_user,prof_id):
    #     designation= request.form.get('Designation')
    #     email= request.form.get('Email')
    #     PhnNo= request.form.get('PhnNo')
    #     token = request.headers['access_token']
    #     data = JWT.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
    #     try: