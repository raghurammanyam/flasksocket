from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,Flask,url_for
from config import db,app
from models.productsmodel import Products
from schemas.productschema import ProductSchema,ProductGetSchema
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import jwt_required
from models.sizemodel import Sizes
import json
from schemas.sizeschema import SizeSchema
app = Flask(__name__,static_url_path='/static',static_folder='/python_bybloss_admin/static')
path = os.getcwd()
UPLOAD_FOLDER = path+'/static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/productslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdateproducts')
loggers = logging.getLogger("consoleproducts")



class IdByProduct(Resource):
    def __init__(self):
        pass
    #@jwt_required
    def get(self,id):
        try:
            product=db.session.query(Products).filter(Products.id==id).first()
            if product:
                schema = ProductGetSchema()
                data = schema.dump(product).data
                logger.info("data feteched successfully based on id ")
                loggers.info("data feteched successfully based on id ")
                return ({"success":True,"data":data})
            else:
                logger.warning("no data found on this id")
                loggers.warning("no data found on this id")
                return ({"success":False,"message":"no data found on this id"})

        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

    #@jwt_required
    def put (self,id):
        try:
            product = request.form.to_dict()
            if 'isActive' in product.keys():
                status=product['isActive']
                product['isActive'] = int(status)
            if 'taxable' in product.keys():
                tax = product['taxable']
                product['taxable'] = int(tax)
            if 'file' not in request.files:
                imagepath = ''
            elif 'file' in request.files:
                file =request.files['file']
                if file.filename == '':
                    imagepath = ''
                if file :
                    def image():
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return url_for("static",filename=filename)
                    imagepath = image()
            if  imagepath != '':
                product['imagePath'] = imagepath
            if 'sizes' in product.keys():
                abc=product.keys()
                if len(abc)==1:
                    sizes =json.loads(product['sizes'])
                    size_put=obj=db.session.query(Sizes).filter(Sizes.productId==id).all()
                    if size_put:
                        for x in size_put:
                         db.session.delete(x)
                         db.session.commit()
                    for x in sizes:
                        x['productId']=id
                        name=x['sizeEn']
                        existing_size = (Sizes.query.filter(Sizes.sizeEn == name).filter(Sizes.productId==id).one_or_none())
                        if existing_size is None:
                            schema_size= SizeSchema()
                            new_size = schema_size.load(x, db.session).data
                            db.session.add(new_size)
                            db.session.commit()

                elif len(abc)>1:
                    request_product = {key:value for key,value in product.items() if key!='sizes'}
                    obj=db.session.query(Products).filter(Products.id==id).update(request_product)
                    if obj:
                        db.session.commit()
                        sizes =json.loads(product['sizes'])
                        size_put=obj=db.session.query(Sizes).filter(Sizes.productId==id).all()
                        if size_put:
                            for x in size_put:
                                db.session.delete(x)
                                db.session.commit()

                        for x in sizes:
                            x['productId']=id
                            name=x['sizeEn']
                            existing_size = (Sizes.query.filter(Sizes.sizeEn == name).filter(Sizes.productId==id).one_or_none())
                            if existing_size is None:
                                schema_size= SizeSchema()
                                new_size = schema_size.load(x, db.session).data
                                db.session.add(new_size)
                                db.session.commit()
            if 'sizes' not in product.keys():
                obj=db.session.query(Products).filter(Products.id==id).update(product)
                if obj:
                    db.session.commit()
            product_detail=db.session.query(Products).filter_by(id=id).one()
            schema = ProductSchema()
            data = schema.dump(product_detail).data
            logger.info("data updated successfully based on id ")
            loggers.info("data updated successfully based on id ")
            return({"success":True,"data":data})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})



    def delete(self,id):
        try:
            product=db.session.query(Products).filter(Products.id==id).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                logger.info("product deleted successfully ")
                loggers.info("product deleted successfully")
                return({"success":True,"message":"product deleted successfully"})
            else:
                logger.warning("product not deleted on this id")
                loggers.warning("product not deleted on this id")
                return({"success":False,"message":"product not deleted on this id"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})
