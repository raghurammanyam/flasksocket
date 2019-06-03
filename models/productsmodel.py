from config import db
import datetime
from models.sizemodel import Sizes


class Products(db.Model):
    __tablename__ = "products"
    id            = db.Column(db.Integer,primary_key=True)
    hid           = db.Column(db.String(255),nullable=True)
    productEn     = db.Column(db.String(255),nullable=True)
    productAr     = db.Column(db.String(255),nullable=True)
    imagePath     = db.Column(db.String(255),nullable=True)
    isActive      = db.Column(db.Boolean, default = True,nullable=True)
    categoryId    = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    createdAt    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updatedAt    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    descEn        = db.Column(db.String(255),nullable=True)
    descAr        = db.Column(db.String(255),nullable=True)
    modifierId    = db.Column(db.Integer, db.ForeignKey('modifiers.id'), nullable = True)
    globalsizeId  = db.Column(db.Integer, db.ForeignKey('globalsizes.id'), nullable = True)
    taxable       = db.Column(db.Boolean, default = True,nullable=True)
    sizes          = db.relationship("Sizes", backref = db.backref('product_size'),uselist=True)
    prices        =db.relationship("Prices",backref=db.backref('product_prices'),lazy='joined',uselist=True)
