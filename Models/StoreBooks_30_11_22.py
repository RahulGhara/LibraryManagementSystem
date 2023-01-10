from DbConnection_30_11_22 import db
# from sqlalchemy.orm import relationship

class Books(db.Model):
    __tablename__ = 'StoreBooks'
    BookID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Author = db.Column(db.String(50))
    Edition = db.Column(db.String(30))
    Price = db.Column(db.Integer)
    # BookAllocation= relationship('BookAllocation',backref='Book', lazy= True)

    def __init__(self, BookID, Name, Author, Edition, Price):
        self.BookID = BookID
        self.Name = Name
        self.Author = Author
        self.Edition = Edition
        self.Price = Price
