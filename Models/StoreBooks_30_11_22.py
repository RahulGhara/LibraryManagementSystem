from DbConnection_30_11_22 import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Books(db.Model):
    __tablename__ = 'StoreBooks'
    BookID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Author = db.Column(db.String(50))
    Edition = db.Column(db.String(30))
    Price = db.Column(db.Integer)
    BooksAvailable=db.Column(db.Integer)
    BookUUID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # BookAllocation= relationship('BookAllocation',backref='Book', lazy= True)

    def __init__(self, BookID, Name, Author, Edition, Price,BooksAvailable,BookUUID):
        self.BookID = BookID
        self.Name = Name
        self.Author = Author
        self.Edition = Edition
        self.Price = Price
        self.BooksAvailable = BooksAvailable
        self.BookUUID = BookUUID
