import pytz
from models import db
from datetime import datetime

time_zone = pytz.timezone("Asia/Tashkent")

class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer(), primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(), nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.now(time_zone))

    def __init__(self, full_name, phone_number, subject, message):
        super().__init__()
        self.full_name = full_name
        self.phone_number = phone_number
        self.subject = subject
        self.message = message

    @staticmethod
    def to_dict(contact):
        _ = {
            "id": contact.id,
            "full_name": contact.full_name,
            "phone_number": contact.phone_number,
            "subject": contact.subject,
            "message": contact.message,
            "created_at": str(contact.created_at)
        }
        return _
