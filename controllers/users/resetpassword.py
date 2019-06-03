from flask import make_response,abort,request
from models.usermodel import Users
from schemas.userschema import user_signupSchema,UsersSchema
from config import *
import random
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.security import generate_password_hash,check_password_hash


class Forget_Password(Resource):
    def __init__(self):
        pass

    def post(self):
        da = request.get_json()
        username = da['username']
        existing_user = db.session.query(Users).filter(Users.username == username).first()
        if existing_user:
            number = random.randint(1000,9999)
            obj = existing_user.username
            id = existing_user.id
            userdata = {"user_id": id,"OTP":number}
            index('Verify Email', username ,'OTP for for your account is :'+ str(number))
            return({"success":True,"data":data})
        else:
            return ({"success":False,"message":"no users with this mailid"})




class Reset_password(Resource):
    def __init__(self):
        pass

    def put(self,id):
            da = request.get_json()
            password= da['password']
            password_hash = generate_password_hash(password)
            dit = {"password": password_hash}
            obj=db.session.query(Users).filter_by(id=id).update(dit)
            if obj:
                db.session.commit()
                abc=db.session.query(Users).filter_by(id=id).one()
                a= abc.__dict__
                schema = UsersSchema()
                username = a['username']
                data = schema.dump(abc).data
                index("mail sent",username,"successfully  Reseted your password")
                return({"success":True,"data":data})
            else:
                return ({"success":False,"message":"no user is available on this id"})
