from models.usermodel import Users
from schemas.userschema import UsersSchema,UsersGetSchema,UsercountSchema
from config import db
from flask_restful import Resource, reqparse
from flask import request
from sqlalchemy import func
import os
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models.ordersmodel import Orders
from models.addressmodel import Addresses
from models.rolemodel import Roles
from schemas.userorderaddressschema import UserAdressSchema

from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/userlogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdateusers')
loggers = logging.getLogger("consoleusers")




class GetUsers(Resource):
    def __init__(self):
        pass
    #@jwt_required
    def get(self):
        try:
            user = db.session.query(Users).filter(Users.roleId==4).order_by(Users.id).all()
            order_count = (db.session.query(Users, func.count(Orders.id).label("num_orders")) .outerjoin(Orders, Users.order).filter(Users.roleId==4).group_by(Users.id))
            total_orders = {b.id:count for b,count in order_count}
            print(total_orders)
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


class GetUpdateUser(Resource):
    def __init__(self):
        pass
    @jwt_required
    def get(self,id):
        try:
            user = Users.query.filter(Users.id == id).one_or_none()
            if user is not None:
                user_schema = UsersGetSchema()
                data = user_schema.dump(user).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("user not found")
                logger.warning("user not found")
                return({"success":False,"message": "user not found"})
        except Exception as e:
            logger.warning(str(e))
            logger.warning(str(e))
            return({"success":False,"message":str(e)})



    # call to update the user details based on user_id
    @jwt_required
    def put(self,id):
        try:
            da = request.get_json()
            user = db.session.query(Users).filter_by(id = id).update(da)
            if user:
                db.session.commit()
                user_obj = Users.query.filter(Users.id == id).one()
                user_schema = UsersSchema()
                data = user_schema.dump(user_obj).data
                logger.info("data updated successfully")
                loggers.info("data updated successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("user not updated")
                loggers.warning("user not updated")
                return({"success":False,"message": "user not updated "})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})



    def delete(self,id):
        try:
            obj=db.session.query(Users).filter(Users.id==id).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("Users deleted successfully")
                loggers.info("Users deleted successfully")
                return("Users deleted successfully")
            else:
                logger.warning("user doesnot deleted")
                loggers.warning("user doesnot deleted")
                return({"success":False,"message": "user doesnot deleted"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})



class GetAllUsers(Resource):
    def __init__(self):
        pass
    #@jwt_required
    def get(self):
        try:
            user = db.session.query(Users).order_by(Users.id).all()
            if user:
                user_schema = UserAdressSchema(many = True)
                data = user_schema.dump(user).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("user not found")
                loggers.warning("user not found")
                return({"success":False,"message": "user not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})
