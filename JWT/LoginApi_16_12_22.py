import datetime
from DbConnection_30_11_22 import app
from flask import request
from Models.Admin_16_12_22 import Admin
import jwt
from Models.Student_6_12_22 import Students
from werkzeug.security import check_password_hash
from logger_16_1_23 import logger


def token_required(f):
    # @wraps
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        # import pdb;pdb.set_trace()
        if 'access_token' in request.headers:
            token = request.headers['access_token']
        if not token:
            return 'token is missing'
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')

            if data.get('ProfID'):
                prof = Admin.query.filter_by(ProfID=data['ProfID']).first()
                current_user = prof
            else:
                student = Students.query.filter_by(UserID=data['UserID']).first()
                current_user = student
        except:
            return 'error!'
        return f(current_user, *args, **kwargs)

    return decorated


def Login():
    logger.debug('Login api is running')
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return 'Error while logging in'
    else:
        logger.debug('fetching admin data')
        admin = Admin.query.filter_by(ProfID=auth.username).first()
        if not admin:
            logger.debug('user is not admin')
            logger.debug('fetching student data')
            student = Students.query.filter_by(UserID=auth.username).first()
            if not student:
                logger.debug('user is not student')
                logger.error('Credential error!')
                return 'no vaild user found!!'
            elif check_password_hash(student.Password, auth.password):
                data = {"UserID": student.UserID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
                token = jwt.encode(data, app.config['SECRET_KEY'])
                logger.debug('token created successfully for student')
                return token
            else:
                logger.error('Password does not match')
                return 'Password does not match'
        elif check_password_hash(admin.Password, auth.password):
        # elif admin.Password == auth.password:
            data = {"ProfID": admin.ProfID,"Email":admin.Email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
            token = jwt.encode(data, app.config['SECRET_KEY'])
            logger.debug('token created successfully for admin')
            return token
        else:
            logger.error('Password does not match')
            return 'Login error! Password does not match'
