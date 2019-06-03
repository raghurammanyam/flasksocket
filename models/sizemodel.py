import os
from flask import Flask
from config import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import datetime
from models.pricemodel import Prices

class Sizes(db.Model):
    __tablename__ = "sizes"
    id         = db.Column(db.Integer,primary_key=True)
    hid  = db.Column(db.String(50),nullable=True)
    sizeEn     = db.Column(db.String(50),nullable=True)
    sizeAr     = db.Column(db.String(50),nullable=True)
    price      = db.Column(db.String(50),nullable=True)
    productId  = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = True)
    createdAt  = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt  = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    taxAmount  = db.Column(db.Float(),nullable=True)
    isActive      = db.Column(db.Boolean, default = True,nullable=True)
    #product = relationship("Parent", back_populates="children")
    prices     =  db.relationship("Prices", backref = db.backref("size_prices"))
