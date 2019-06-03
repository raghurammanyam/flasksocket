from models.usermodel import Users
from schemas.userschema import user_signupSchema
from flask_restful import Resource
from config import *
from flask import request,session
from werkzeug.security import check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models.revokemodel import *
import datetime


from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/userlogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('signup_users')
loggers = logging.getLogger("consoleusers")




class SecretResource(Resource):
    @jwt_required
    def get(self):
        return ("success")



class Signin(Resource):
    def __init__(self):
        pass

    # login call for the user
    def post(self):
        try:
            sign_in = request.get_json()
            username = sign_in['username']
            password = sign_in['password']
            username_check = db.session.query(Users).filter(Users.username == username).first()
            if username_check is not None:
                schema = user_signupSchema()
                data   = schema.dump(username_check).data
                hashed_password = username_check.password
                if check_password_hash(hashed_password,password):
                    expires = datetime.timedelta(hours=2)
                    access_token = create_access_token(identity = username,expires_delta=expires)
                    refresh_token = create_refresh_token(identity = username)
                    logger.info("user sigin successfully")
                    loggers.info("user sigin successfully")
                    return {"success":True,
                        'data':data,
                        'message': 'logined successfully',

                        'access_token': access_token,
                        'refresh_token': refresh_token
                        }
                else:
                    logger.warning("Invalid password")
                    loggers.warning("Invalid password")
                    return({"success":False,"message": "Invalid password"})
            else:
                logger.warning("Invalid UserName")
                loggers.warning("Invalid UserName")
                return({"success":False,"message": "Invalid UserName"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


class UserLogoutAccess(Resource):
   @jwt_required
   def post(self):
       jti = get_raw_jwt()['jti']
       revoked_token = RevokedTokenModel(jti = jti)
       revoked_token.add()
       return {'message': 'Access token has been revoked'}

class UserLogoutRefresh(Resource):
   @jwt_refresh_token_required
   def post(self):
       jti = get_raw_jwt()['jti']
       revoked_token = RevokedTokenModel(jti = jti)
       revoked_token.add()
       return {'message': 'Refresh token has been revoked'}
