from config import db
import datetime







class Prices(db.Model):
    __tablename__ ='prices'
    id            = db.Column(db.Integer,primary_key=True)
    sizeId        = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable = True)
    productId     = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = True)
    price         = db.Column(db.String(255),nullable=True)
    createdAt     = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt     = db.Column(db.DateTime, default = datetime.datetime.utcnow())