from config import db
import datetime
from datetime import datetime







class Orders(db.Model):
    __tablename__ ='orders'

    id             =  db.Column(db.Integer ,primary_key = True)
    hid            =  db.Column(db.String(255),nullable=True)
    userId         =  db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    price          =  db.Column(db.String(255),nullable=True)
    discount       =  db.Column(db.String(255),nullable=True)
    deliveryPrice  =  db.Column(db.String(255),nullable=True)
    finalPrice     =  db.Column(db.String(255),nullable=True)
    orderType      =  db.Column(db.String(255),nullable=True)
    orderStatus    =  db.Column(db.String(255),nullable=True)
    placedOn       =  db.Column(db.Date,default = datetime.date(datetime.now()),nullable=True)
    taxAmount      =  db.Column(db.String(255),nullable=True)
    branchHid      =  db.Column(db.String(255),nullable=True)
    posReference   =  db.Column(db.String(255),nullable=True)
    createdAt      =  db.Column(db.DateTime,default = datetime.utcnow())
    updatedAt      =  db.Column(db.DateTime,default = datetime.utcnow())
