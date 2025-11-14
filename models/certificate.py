import pytz
from models import db
from datetime import datetime

time_zone = pytz.timezone("Asia/Tashkent")

class Certificate(db.Model):
    __tablename__ = "certificate"

    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    file_path = db.Column(db.Text(), nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.now(time_zone))

    def __init__(self, title, description, file_path):
        super().__init__()
        self.title = title
        self.description = description
        self.file_path = file_path

    @staticmethod
    def to_dict(certificate):
        _ = {
            "id": certificate.id,
            "title": certificate.title,
            "description": certificate.description,
            "file_path": certificate.file_path,
            "created_at": str(certificate.created_at)
        }
        return _
