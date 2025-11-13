import pytz
from models import db
from datetime import datetime
from flask_bcrypt import generate_password_hash

time_zone = pytz.timezone("Asia/Tashkent")

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.now(time_zone))

    def __init__(self, full_name, phone_number, username, password):
        super().__init__()
        self.full_name = full_name
        self.phone_number = phone_number
        self.username = username
        self.password = generate_password_hash(password).decode("utf-8")

    @staticmethod
    def to_dict(user):
        _ = {
            "id": user.id,
            "full_name": user.full_name,
            "phone_number": user.phone_number,
            "username": user.username,
            "created_at": str(user.created_at)
        }
        return _
