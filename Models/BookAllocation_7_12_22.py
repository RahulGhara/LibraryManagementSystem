from DbConnection_30_11_22 import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class BookAllocation(db.Model):
    __tablename__ = 'BookAllocationTable'
    StudentBookAllocationID = db.Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    StudentID = db.Column(UUID(as_uuid=True), db.ForeignKey("Student.StudentID"), nullable=False, default=uuid.uuid4)
    BookID = db.Column(db.Integer, nullable=False)
    IssueDate = db.Column(db.Date, nullable=False)
    IssueEndDate = db.Column(db.Date, nullable=False)
    BookAllocationStatus = db.Column(db.String(40))

    def __init__(self, StudentBookAllocationID, StudentID, RollNo, BookID, IssueDate, IssueEndDate,
                 BookAllocationStatus):
        self.StudentBookAllocationID = StudentBookAllocationID
        self.StudentID = StudentID
        self.RollNo = RollNo
        self.BookID = BookID
        self.IssueDate = IssueDate
        self.IssueEndDate = IssueEndDate
        self.BookAllocationStatus = BookAllocationStatus
