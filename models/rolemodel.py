import os
from flask import Flask
from config import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import datetime
from models.usermodel import Users

class Roles(db.Model):
    __tablename__ = "roles"
    id         = db.Column(db.Integer,primary_key=True)
    role       = db.Column(db.String(50),nullable=True)
    createdAt = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    User      =  db.relationship("Users", backref = db.backref("Role_user"))
