from config import db
import datetime





class Addresses(db.Model):
    __tablename__ = "addresses"

    id              = db.Column(db.Integer,primary_key=True)
    address         = db.Column(db.String(255),nullable=True)
    latitude        = db.Column(db.String(255),nullable=True)
    longitude       = db.Column(db.String(255),nullable=True)
    userId          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)
    # deliveryzoneId  = db.Column(db.Integer, db.ForeignKey('deliveryzones.id'), nullable = True)
    createdAt       = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt       = db.Column(db.DateTime, default = datetime.datetime.utcnow(),onupdate=datetime.datetime.utcnow())
    type            = db.Column(db.String(255),nullable=True)
    isActive      = db.Column(db.Boolean, default = True,nullable=True)
