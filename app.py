# import gevent.monkey

# gevent.monkey.patch_all()
from flask import Flask
from config import app,socketio,db
from flask_restful import Api
from flask_cors import CORS
import os
import datetime
from flask import Flask
from flask_seeder import FlaskSeeder
# from flask_socketio import SocketIO
from websockets import handle_message,handle_json,handle_my_custom_event,handle_message,handle_json,handle_my_custom_event




api = Api(app)

CORS(app)


app.config.from_object(os.environ['APP_SETTINGS'])
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


       # roles api calls endpoints

from controllers.roles.postroles import Getcreateroles
from controllers.roles.getupdatedeleteroles import GetUpdateDeleteRoles

api.add_resource(Getcreateroles, '/api/addrole')
api.add_resource(GetUpdateDeleteRoles, '/api/getupdatedeleteroles/<int:id>')


        # permission api calls endpoints

from controllers.users.user_signin import Signin,SecretResource,UserLogoutAccess,UserLogoutRefresh
from controllers.users.user_signup import Signup
from controllers.users.getupdatedeleteuser import GetUpdateUser ,GetAllUsers
from controllers.users.resetpassword import Forget_Password,Reset_password
from controllers.users.myaccountdetails import MyAccountDetails

api.add_resource(Signup,'/users')
api.add_resource(Signin,'/login')
#api.add_resource(GetUsers,'/users')
api.add_resource(GetAllUsers,'/api/getalluser')
api.add_resource(GetUpdateUser,'/api/getupdateuser/<int:id>')
api.add_resource(Forget_Password,'/api/forgetpassword')
api.add_resource(Reset_password,'/api/resetpassword/<int:id>')
api.add_resource(SecretResource,'/api/secretresource')
api.add_resource(UserLogoutAccess,'/api/userlogoutaccess')
api.add_resource(UserLogoutRefresh,'/api/userlogoutrefresh')
api.add_resource(MyAccountDetails,'/api/accountdetails/<int:id>')


        # globalsize Api calls endpoints

from controllers.globalsize.postglobalsize import GetcreateGlobalSize
from controllers.globalsize.getupdateglobalsize import GetUpdateDeleteGlobalSize

api.add_resource(GetcreateGlobalSize, '/api/addglobalsize')
api.add_resource(GetUpdateDeleteGlobalSize, '/api/getupdateglobalsize/<int:id>')


        # addresses api calls endpoints

from controllers.addresses.postaddress import PostAddress
from controllers.addresses.address_by_id import AdressByID

api.add_resource(PostAddress,'/api/createaddress')
api.add_resource(AdressByID,'/api/getupdateaddress/<int:id>')


       # categorie api calls endpoints

from controllers.categories.postcategories import CategoriesPost,CategoriesSearch
from controllers.categories.categorie_by_id import IdByCategorie



api.add_resource(CategoriesPost,'/categories')
api.add_resource(IdByCategorie,'/api/updatecategorie/<int:id>')
api.add_resource(CategoriesSearch,'/api/categorysearch')

    # product api calls endpoints

from controllers.products.postproducts import ProductsPost,ProductSearch
from controllers.products.product_by_id import IdByProduct
from controllers.products.productstatus import GetProductSizeStatus

#api.add_resource(PostProducts,'/products')

api.add_resource(ProductsPost,'/products')
api.add_resource(IdByProduct,'/api/updateproduct/<int:id>')
api.add_resource(GetProductSizeStatus,'/api/getproductsize')
api.add_resource(ProductSearch,'/api/productsearch')

    # order api calls endpoints

from controllers.orders.postorders import PostOrders
from controllers.orders.orders_by_id import OrderById,OrderByuser
#from controllers.orders.orderinvoice import orderInvoice


api.add_resource(PostOrders,'/orders')
api.add_resource(OrderById,'/api/getupdateorder/<int:id>')
api.add_resource(OrderByuser,'/api/getorderbyuserid/<int:id>')
#api.add_resource(orderInvoice,'/api/orderinvoice')



    # price api calls endpoints

from controllers.prices.postprices import PostPrices
api.add_resource(PostPrices,'/api/createprice')


    # size api calls endpoint

from controllers.sizes.postsize import  Getcreatesize
from controllers.sizes.getupdatesize import GetUpdateDeleteSizes

api.add_resource(Getcreatesize,'/api/createsize')
api.add_resource(GetUpdateDeleteSizes,'/api/getupdatesize/<int:id>')

        # DashBoard api calls endpoints

from controllers.admindashboard.dashboardcalls import DashBoardcalls
from controllers.admindashboard.dashboardday import DashBoardday
from controllers.admindashboard.dashgraph import Dashgraph
from controllers.admindashboard.dashboardpie import DashBoardpie

api.add_resource(DashBoardcalls,'/barchart/top')
api.add_resource(DashBoardday,'/api/dashboardday')
api.add_resource(Dashgraph,'/barchart')
api.add_resource(DashBoardpie,'/api/dashboardpie')



from flask_jwt_extended import JWTManager
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=2)
jwt = JWTManager(app)



from models.revokemodel import RevokedTokenModel as b

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return b.is_jti_blacklisted(jti)

seeder = FlaskSeeder()
seeder.init_app(app, db)

if __name__ == "__main__":
   # app.run()
    socketio.run(app)
