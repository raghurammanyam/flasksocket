from models.usermodel import Users
from schemas.userschema import user_signupSchema,UsersSchema,UsersSchemas
from config import *
from flask import request, make_response, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash
import os
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from config import db,basedir
import logging, logging.config, yaml
from sqlalchemy import func
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models.ordersmodel import Orders
from models.addressmodel import Addresses
from models.rolemodel import Roles
from schemas.userorderaddressschema import UserAdressSchema
from schemas.userschema import UsersSchema,UsersGetSchema,UsercountSchema

CONFIG_PATH = os.path.join(basedir,'loggeryaml/userlogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('signin_users')
loggers = logging.getLogger("consoleusers")


@jwt_required
def get(self):
    pass

class Signup(Resource):
    def __init__(self):
        pass

    def get(self):
        try:
            user = db.session.query(Users).filter(Users.roleId==4).order_by(Users.id).all()
            order_count = (db.session.query(Users, func.count(Orders.id).label("num_orders")) .outerjoin(Orders, Users.order).filter(Users.roleId==4).group_by(Users.id))
            total_orders = {b.id:count for b,count in order_count}
            total_amount = (db.session.query(Users, func.sum(Orders.finalPrice).label("total_amount")) .outerjoin(Orders, Users.order).filter(Users.roleId==4).group_by(Users.id))
            user_amount  =  {b.id:total for b,total in total_amount}
            address_count = (db.session.query(Users, func.count(Addresses.id).label("num_address")) .outerjoin(Addresses, Users.address).filter(Users.roleId==4).group_by(Users.id))
            user_address = {b.id:count for b,count in address_count}

            if user:
                user_schema = UsercountSchema(many = True)
                data = user_schema.dump(user).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return({"success":True,"data":data,"total_orders":total_orders,"user_amount":user_amount,"user_address":user_address})
            else:
                logger.warning("user not found")
                loggers.warning("user not found")
                return({"success":False,"message": "user not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    def post(self):
        try:
            post_user = request.get_json()
            name=post_user['name']
            username = post_user['username']
            password = post_user['password']
            mobile=post_user["mobile"]
            #dictionary[new_key] = dictionary.pop(old_key)
            dict={"username":username,"password":password,"name":name,"mobileNumber":mobile}
            #dit =  {key:value for key,value in post_user.items()}
            #print(dit)
            #dit[mobileNumber] = dit.pop(mobile)
            #print(dit)
            username_id  = db.session.query(Users).filter(Users.username == username).first()
            if username_id is None:
                hash_password = generate_password_hash(password)
                schema = user_signupSchema()
                new_signup = schema.load(dict, session = db.session).data
                new_signup.password = hash_password
                db.session.add(new_signup)
                db.session.commit()
                access_token = create_access_token(identity = username)
                refresh_token = create_refresh_token(identity = username)
                schema = UsersSchemas()
                user = db.session.query(Users).filter(Users.username == username).one()
                data = schema.dump(new_signup).data
                logger.info("user signup successfully")
                loggers.info("user signup successfully")
                return {'success':True,
                    'message': 'Users {} was created'.format(username),
                    'access_token' : access_token,
                    'refresh_token': refresh_token,
                    'data'         : data
                    }
            else:
                logger.warning("email already exists")
                loggers.warning("email already exists")
                return ({"success":False,"message":"email already exists"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})
