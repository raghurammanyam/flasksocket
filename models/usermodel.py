import os
from flask import Flask
from config import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import datetime
from models.ordersmodel import Orders
from models.addressmodel import Addresses


 # user models

class Users(db.Model):
    __tablename__ = "users"
    id             = db.Column(db.Integer,primary_key=True)
    hid            = db.Column(db.String(50),nullable=True)
    name           = db.Column(db.String(50),nullable=True)
    loginFrom      = db.Column(db.String(50),nullable=True)
    type           = db.Column(db.String(50),nullable=True)
    roleId         = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable = True)
    mobileNumber   = db.Column(db.String(10),nullable = True)
    username       = db.Column(db.String(120), unique = True, nullable = False)
    password       = db.Column(db.String(246))
    address        = db.Column(db.Text(),nullable = True)
    isActive      = db.Column(db.Boolean, default = True,nullable=True)
    createdAt      = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt      = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    order          = db.relationship("Orders", backref = db.backref("user_order"),uselist=True)
    address        = db.relationship("Addresses", backref = db.backref("user_address"),uselist=True)
