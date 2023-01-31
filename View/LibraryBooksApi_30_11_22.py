import uuid
import re
from flask import request
from DbConnection_30_11_22 import db, app
from Models.StoreBooks_30_11_22 import Books
from JWT.LoginApi_16_12_22 import token_required
import jwt
from logger_16_1_23 import logger

class StoreBooksApi:
    @staticmethod
    @token_required
    def AddBook(current_user):
        logger.debug('AddBook api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            logger.debug('This is in the authentication block now')
            if data["ProfID"]:
                book_id_pattern = r'^BK\B[_]([A-Z]{1})[_][0-9]{3,5}$'
                BookID = request.form.get('BookID')
                Name = request.form.get('Name')
                Author = request.form.get('Author')
                Edition = request.form.get('Edition')
                Price = request.form.get('Price')
                BooksAvailable = request.form.get('BooksAvailable')
                Bookuuid= uuid.uuid4()
                logger.debug('Checking book_id pattern')
                if re.match(book_id_pattern,BookID):
                    new_book = Books(BookID, Name, Author, Edition, Price,BooksAvailable,Bookuuid)
                    db.session.add(new_book)
                    db.session.commit()
                    logger.debug('New entry created')
                    return "New book is now available in library"
                else:
                    logger.error('BookID format is not matching')
                    return "BookID format is not matching"
        except:
            logger.error('Token is not authorized')
            return "Unauthorized Person"

    @staticmethod
    def ViewBook(book_id):
        logger.debug('ViewBook api is running')
        book = Books.query.filter_by(BookID=book_id).first()
        if book:
            record = [book.BookID, book.Name, book.Author, book.Edition, book.Price, book.BookUUID]
            return record
        else:
            logger.error('BookID is not present in the database')
            return 'not exist'

    @staticmethod
    @token_required
    def ViewAll(current_user):
        logger.debug('ViewAll api is running')
        books = Books.query.all()
        all_books = []
        for item in books:
            record = {
                'BookID': item.BookID,
                'Name': item.Name,
                'Author': item.Author,
                'Edition': item.Edition,
                'Price': item.Price,
            }
            all_books.append(record)
        return all_books

    @staticmethod
    @token_required
    def DeleteBook(current_user, book_id):
        logger.debug('DeleteBook api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            logger.debug('This is in the authentication block now')
            if data["ProfID"]:
                record = Books.query.filter_by(BookID=book_id).first()
                if record:
                    db.session.delete(record)
                    db.session.commit()
                    logger.debug('record deleted')
                    return 'Book deleted'
                else:
                    logger.debug('No record found for such book_id')
                    return 'BookID not found'
        except:
            logger.error('Token is not authorized')
            return "You are not authorized to access this"

    @staticmethod
    @token_required

    def UpdateBook(current_user, book_id):
        logger.debug('UpdateBook api is running')
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        # breakpoint()
        try:
            logger.debug('This is in the authentication block now')
            book = Books.query.filter_by(BookID=book_id).first()
            if book:
                if data["ProfID"]:
                    # print(type(book))
                    new_name = request.form.get('Name')
                    new_author = request.form.get('Author')
                    new_edition = request.form.get('Edition')
                    new_price = request.form.get('Price')
                    if new_name == None and new_author == None and new_edition == None and new_price == None:
                        return "No fields are given to update"
                    elif new_name == '' or new_author == '' or new_edition == '' or new_price == '':
                        return " give values to all fields"
                    else:
                        if new_name:
                            book.Name = new_name
                        if new_author:
                            book.Author = new_author
                        if new_edition:
                            book.Edition = new_edition
                        if new_price:
                            book.Price = new_price
                        db.session.commit()
                        logger.debug('record updated')
                        return "updated"
            else:
                logger.error('BookID is wrong')
                return 'BookID is wrong'
        except:
            logger.debug('Token is not authorized')
            return 'You are not authorized to access this'
