from flask import request
from DbConnection_30_11_22 import db, app
from Models.StoreBooks_30_11_22 import Books
from JWT.LoginApi_16_12_22 import token_required
import jwt


class StoreBooksApi:
    @staticmethod
    @token_required
    def AddBook(current_user):
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            if data["ProfID"]:
                BookID = request.form.get('BookID')
                Name = request.form.get('Name')
                Author = request.form.get('Author')
                Edition = request.form.get('Edition')
                Price = request.form.get('Price')
                new_book = Books(BookID, Name, Author, Edition, Price)
                db.session.add(new_book)
                db.session.commit()
                return "New book is now available in library"
        except:
            return "Unauthorized Person"

    @staticmethod
    def ViewBook(book_id):
        book = Books.query.get(book_id)
        if book != None:
            record = [book.BookID, book.Name, book.Author, book.Edition, book.Price]
            return record
        else:
            return 'not exist'

    @staticmethod
    @token_required
    def ViewAll(current_user):
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
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            if data["ProfID"]:
                record = Books.query.get(book_id)
                if record:
                    db.session.delete(record)
                    db.session.commit()
                    return 'Book deleted'
                else:
                    return 'BookID not found'
        except:
            return "You are not authorized to access this"

    @staticmethod
    @token_required
    def UpdateBook(current_user, book_id):
        token = request.headers['access_token']
        data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
        try:
            if data["ProfID"]:
                book = Books.query.get(book_id)
                new_name = request.form.get('Name')
                new_author = request.form.get('Author')
                new_edition = request.form.get('Edition')
                new_price = request.form.get('Price')
                if new_name == None and new_author == None and new_edition == None and new_price == None:
                    return "No fields are given to update"
                elif new_name == '' or new_author == '' or new_edition == '' or new_price == '':
                    return " give values to all fields"
                elif new_name == None and new_author == None and new_edition == None:
                    book.Price = new_price
                    db.session.commit()
                    return "updated"
                elif new_author == None and new_edition == None and new_price == None:
                    book.Name = new_name
                    db.session.commit()
                    return "updated"
                elif new_edition == None and new_price == None and new_name == None:
                    book.Author = new_author
                    db.session.commit()
                    return "updated"
                elif new_name == None and new_author == None and new_price == None:
                    book.Edition = new_edition
                    db.session.commit()
                    return "updated"
                elif new_name == None and new_author == None:
                    book.Edition = new_edition
                    book.Price = new_price
                    db.session.commit()
                    return "updated"
                elif new_edition == None and new_price == None:
                    book.Name = new_name
                    book.Author = new_author
                    db.session.commit()
                    return "updated"
                elif new_name == None and new_price == None:
                    book.Edition = new_edition
                    book.Author = new_author
                    db.session.commit()
                    return "updated"
                elif new_edition == None and new_name == None:
                    book.Author = new_author
                    book.Price = new_price
                    db.session.commit()
                    return "updated"
                elif new_price == None and new_author == None:
                    book.Edition = new_edition
                    book.Name = new_name
                    db.session.commit()
                    return "updated"
                elif new_edition == None and new_author == None:
                    book.Name = new_name
                    book.Price = new_price
                    db.session.commit()
                    return "updated"
                elif new_name == None:
                    book.Edition = new_edition
                    book.Author = new_author
                    book.Price = new_price
                    db.session.commit()
                    return "updated"
                elif new_edition == None:
                    book.Name = new_name
                    book.Author = new_author
                    book.Price = new_price
                    db.session.commit()
                    return "updated"
                elif new_author == None:
                    book.Edition = new_edition
                    book.Name = new_name
                    book.Price = new_price
                    db.session.commit()
                    return "updated"
                elif new_price == None:
                    book.Edition = new_edition
                    book.Author = new_author
                    book.Name = new_name
                    db.session.commit()
                    return "updated"
                else:
                    book.Name = new_name
                    book.Edition = new_edition
                    book.Author = new_author
                    book.Name = new_name
                    db.session.commit()
                    return "updated"
        except:
            return 'You are not authorized to access this'
