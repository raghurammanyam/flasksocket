from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow
import datetime
from models.productsmodel import Products
from config import db


class GlobalSizes(db.Model):
    __tablename__ = "globalsizes"

    id            = db.Column(db.Integer,primary_key=True)
    sizeEn        = db.Column(db.String(255),nullable=True)
    sizeAr        = db.Column(db.String(255),nullable=True)
    updatedAt    = db.Column(db.DateTime, default = datetime.datetime.utcnow(),nullable=True)
    createdAt    = db.Column(db.DateTime, default = datetime.datetime.utcnow(),nullable=True)
    Product      = db.relationship("Products", backref = db.backref('globalsize_product'))
