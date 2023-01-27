import uuid
from Models.StoreBooks_30_11_22 import Books
from Models.BookAllocation_7_12_22 import BookAllocation
from Models.Student_6_12_22 import Students
from flask import request
from DbConnection_30_11_22 import db
from JWT.LoginApi_16_12_22 import token_required
import jwt
from DbConnection_30_11_22 import app
from logger_16_1_23 import logger
import datetime


class BookAllocationApi:
    @staticmethod
    @token_required
    def AllocateBook(current_user, roll_no):
        logger.debug('AllocateBook api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        logger.debug('entering in the authentication block')
        try:
            # breakpoint()
            if data['ProfID']:
                student = Students.query.filter_by(RollNo=roll_no).first()
                if student:
                    logger.debug('student found')
                    student_book_allocation_id = uuid.uuid4()
                    student_id = student.StudentID
                    book = request.form.get('BookID')
                    if Books.query.filter_by(BookID= book).first():
                        book_id = book
                    else:
                        logger.error('BookID not found')
                        return 'No book found'
                    issue_date = datetime.datetime.now()
                    # date_to_add= 15
                    issue_end_date = (datetime.date.today()+ datetime.timedelta(days=15))
                    # return_time = (issue_date.strftime("%H:%M:%S"))
                    return_time= None
                    BookAllocationStatus = request.form.get('Status')
                    # student_record= Students.query.filter_by(RollNo=roll_no).first()
                    book_store_record = Books.query.filter_by(BookID=book_id).first()
                    if book_store_record.BooksAvailable > 0:
                        book_store_record.BooksAvailable = book_store_record.BooksAvailable - 1
                        new_entry = BookAllocation(student_book_allocation_id, student_id, book_id, issue_date,
                                                   issue_end_date, return_time, BookAllocationStatus)
                        db.session.add(new_entry)
                        db.session.commit()
                        logger.debug('Book allocated')
                        return 'Book allocation successful'
                    else:
                        logger.warning('Book is not available in book store')
                        return 'Book is not available'
                else:
                    logger.error('Student rollNo not found')
                    return 'No student found for such RollNo'
        except:
            logger.error('user is not authorized')
            return 'You are not authorized to access this'

    @staticmethod
    @token_required
    def BookReturn(current_user, roll_no):
        logger.debug('StatusUpdate api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')

        # breakpoint()
        try:
            logger.debug('In the authentication block')
            if data['ProfID']:
                student = Students.query.filter_by(RollNo=roll_no).first()
                if student:
                    logger.debug('student found')
                    book = request.form.get('BookID')
                    book_allocation_record = BookAllocation.query.filter_by(StudentID=student.StudentID,
                                                                            BookID=book).first()
                    if book_allocation_record:
                        if book_allocation_record.BookAllocationStatus == 'Issued':
                            book_allocation_record.BookAllocationStatus = request.form.get('Status')
                            book_store_record = Books.query.filter_by(BookID=book).first()
                            book_store_record.BooksAvailable = book_store_record.BooksAvailable + 1
                            book_allocation_record.ReturnTime = (datetime.datetime.now().strftime("%H:%M:%S"))
                            # book_allocation_record.ReturnTime = datetime.datetime.now()
                            db.session.commit()
                            logger.debug('The record is updated and deleted')
                            return 'status updated'
                        else:
                            return 'Book is already returned'
                    else:
                        logger.error('record not found')
                        return 'Book is not allocated'
                else:
                    logger.error('No student found')
                    return 'No student found'
        except:
            logger.error('user is not authorized')
            return 'You are not authorized to access this'

    @staticmethod
    def ViewDetails(roll_no):
        logger.debug('ViewDetails api is running')
        student = Students.query.filter_by(RollNo=roll_no).first()
        if student:
            student_id = BookAllocation.query.filter_by(StudentID=student.StudentID).all()
            list_of_records = []
            for std in student_id:
                record = {'Book_id': std.BookID, 'Issue_date': std.IssueDate,
                          'Issue_end_date': std.IssueEndDate}
                list_of_records.append(record)
            if list_of_records == []:
                logger.warning('No book allocated')
                return 'No book allocated to this student'
            else:
                return list_of_records
        else:
            logger.error('No student found')
            return "no student found"
