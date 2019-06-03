from config import db
import datetime
from models.productsmodel import Products
from sqlalchemy.orm import relationship





class Categories(db.Model):
    __tablename__ = "categories"

    id            = db.Column(db.Integer,primary_key=True)
    hid           = db.Column(db.String(255),nullable=True)
    categoryEn    = db.Column(db.String(255),nullable=True)
    categoryAr    = db.Column(db.String(255),nullable=True)
    imagePath     = db.Column(db.String(255),nullable=True)
    isActive      = db.Column(db.Boolean, default = True,nullable=True)
    createdAt    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    products     = db.relationship("Products", backref = db.backref('category'),uselist=True)
