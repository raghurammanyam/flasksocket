
from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Welcome@123@104.199.146.29/python_byblos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class RevokedTokenModel(db.Model):
     __tablename__ = 'revoked_tokens'
     id = db.Column(db.Integer, primary_key = True)
     jti = db.Column(db.String(120))

     def add(self):
         db.session.add(self)
         db.session.commit()

     @classmethod
     def is_jti_blacklisted(cls, jti):
         query = cls.query.filter_by(jti = jti).first()
         return bool(query)


# db.create_all()
# db.session.commit()
