from config import db
import datetime
from models.addressmodel import Addresses




class Deliveryzones(db.Model):
    __tablename__ = "deliveryzones"

    id                  = db.Column(db.Integer,primary_key=True)
    hid                 = db.Column(db.String(255),nullable=True)
    name                = db.Column(db.String(255),nullable=True)
    latitude            = db.Column(db.String(255),nullable=True)
    longitude           = db.Column(db.String(255),nullable=True)
    branchId            = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable = True)
    createdAt           = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt           = db.Column(db.DateTime, default = datetime.datetime.utcnow(),onupdate=datetime.datetime.utcnow())
    delivery_address    = db.relationship("Addresses", backref = db.backref('address_delivery'),uselist=True)
