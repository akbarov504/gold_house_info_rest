import pytz
from models import db
from datetime import datetime

time_zone = pytz.timezone("Asia/Tashkent")

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image_path = db.Column(db.Text(), nullable=False)
    proba = db.Column(db.Integer(), nullable=False)
    gramm = db.Column(db.Float(), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.now(time_zone))

    def __init__(self, title, description, image_path, proba, gramm, type):
        super().__init__()
        self.title = title
        self.description = description
        self.image_path = image_path
        self.proba = proba
        self.gramm = gramm
        self.type = type

    @staticmethod
    def to_dict(product):
        _ = {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "image_path": product.image_path,
            "proba": product.proba,
            "gramm": product.gramm,
            "type": product.type,
            "created_at": str(product.created_at)
        }
        return _
