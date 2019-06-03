from config import db
import datetime
from models.productsmodel import Products



class Modifiers(db.Model):
    __tablename__ = "modifiers"
    id            = db.Column(db.Integer,primary_key=True)
    hid     = db.Column(db.String(255),nullable=True)
    enName        = db.Column(db.String(255),nullable=True)
    arName        = db.Column(db.String(255),nullable=True)
    isMultiple    = db.Column(db.String(255),nullable=True)
    createdAt     = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt     = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    Product       =  db.relationship("Products", backref = db.backref("modifier_product"))
