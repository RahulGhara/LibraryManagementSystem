import uuid
from Models.StoreBooks_30_11_22 import Books
from Models.BookAllocation_7_12_22 import BookAllocation
from Models.Student_6_12_22 import Students
from flask import request
from DbConnection_30_11_22 import db
from JWT.LoginApi_16_12_22 import token_required
import jwt
from DbConnection_30_11_22 import app


class BookAllocationApi:
    @staticmethod
    @token_required
    def AllocateBook(current_user, roll_no):
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            if data['ProfID']:
                student = Students.query.filter_by(RollNo=roll_no).first()
                if student:

                    student_book_allocation_id = uuid.uuid4()
                    student_id = student.StudentID
                    book = request.form.get('BookID')
                    if Books.query.get(book):
                        book_id = book
                    else:
                        return 'No book found'
                    date = request.form.get('IssueDate')
                    # BookAllocation.IssueDate.set(date)
                    # upto = datetime.timedelta(days=15)
                    # issue_end_date = date + upto
                    # BookAllocation.IssueEndDate.set(issue_end_date)
                    issue_end_date = request.form.get('IssueEndDate')
                    BookAllocationStatus = request.form.get('Status')
                    new_entry = BookAllocation(student_book_allocation_id, student_id, roll_no, book_id, date, issue_end_date,
                                               BookAllocationStatus)
                    db.session.add(new_entry)
                    db.session.commit()
                    return 'Book allocation successful'
                else:
                    return 'No student found for such RollNo'
        except:
            return 'You are not authorized to access this'

    @staticmethod
    @token_required
    def StatusUpdate(current_user, roll_no):
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            if data['ProfID']:
                student = Students.query.filter_by(RollNo=roll_no).first()
                if student:
                    book = request.form.get('BookID')
                    book_allocation_record = BookAllocation.query.filter_by(StudentID=student.StudentID, BookID=book).first()
                    if book_allocation_record:
                        if book_allocation_record.BookAllocationStatus == 'Issued':
                            book_allocation_record.BookAllocationStatus = request.form.get('Status')
                            db.session.commit()
                            return 'status updated'
                        else:
                            return 'Book is already returned'
                    else:
                        return 'Book is not allocated'
                else:
                    return 'No student found'
        except:
            return 'You are not authorized to access this'

    @staticmethod
    def ViewDetails(roll_no):
        student = Students.query.filter_by(RollNo=roll_no).first()
        if student:
            student_id = BookAllocation.query.filter_by(StudentID=student.StudentID).all()
            list=[]
            for std in student_id:
                record = {'Book_id': std.BookID, 'Issue_date': std.IssueDate,
                           'Issue_end_date': std.IssueEndDate}
                list.append(record)
            if list ==[]:
                return 'No book allocated to this student'
            else:
                return list
        else:
            return "no student found"
