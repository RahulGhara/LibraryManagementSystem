from DbConnection_30_11_22 import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Admin(db.Model):
    __tablename__ = 'Admin'
    ID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Name = db.Column(db.String(100))
    ProfID = db.Column(db.String(50),unique=True)
    Password = db.Column(db.String(1000),unique=True)
    Designation = db.Column(db.String(40), nullable=False)
    Email = db.Column(db.String(50),nullable=False)
    PhnNo=db.Column(db.BIGINT, nullable=False)

    def __init__(self,ID,Name,ProfID,Password,Designation,Email,PhnNo):
        self.ID=ID
        self.Name=Name
        self.ProfID=ProfID
        self.Password=Password
        self.Designation=Designation
        self.Email= Email
        self.PhnNo=PhnNo