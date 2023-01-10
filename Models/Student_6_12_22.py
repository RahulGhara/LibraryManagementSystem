from DbConnection_30_11_22 import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from Models.BookAllocation_7_12_22 import BookAllocation
class Students(db.Model):
    __tablename__ = 'Student'
    StudentID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    RollNo = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Department = db.Column(db.String(50), nullable=False)
    Semester = db.Column(db.String(30), nullable=False)
    PassoutYear = db.Column(db.Integer, nullable=False)
    UserID = db.Column(db.String(40),unique=True,nullable=False)
    Password = db.Column(db.String(1000),unique=True,nullable=False)
    Email = db.Column(db.String(80),unique=True,nullable=False)
    PhnNo = db.Column(db.BIGINT,unique=True,nullable=False)
    BookAllocation = db.relationship('BookAllocation', backref='Student', lazy=True)

    def __init__(self, StudentID, RollNo, Name, Department, Semester, PassoutYear, UserID, Password, Email, PhnNo):
        self.StudentID = StudentID
        self.RollNo = RollNo
        self.Name = Name
        self.Department = Department
        self.Semester = Semester
        self.PassoutYear = PassoutYear
        self.UserID = UserID
        self.Password = Password
        self.Email = Email
        self.PhnNo = PhnNo
