from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request
from config import db
from models.ordersmodel import Orders
from schemas.ordersschema import OrderGetSchema
from flask import Flask, render_template,Response
from config import *
from flask_mail import Mail, Message
from Services import Email


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bhanuchander008@gmail.com'
app.config['MAIL_PASSWORD'] = 'abhi1015'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def index(subject, email, body):
   order_data = db.session.query(Orders).order_by(Orders.id).first()
   print("?>>>>>>?",order_data)
   msg = Message(subject, sender = 'bhanuchander008@gmail.com', recipients = [email])
   msg.body = body
   msg.html = render_template('byblosInvoice.html',order_data=order_data)

   mail.send(msg)
   return "successfully sent"

class orderInvoice(Resource):

    def get(self):
        try:
             order_data = db.session.query(Orders).order_by(Orders.id).first()
             res = render_template('byblosInvoice.html',order_data=order_data)
             v = Email()
             v.MailGrid(sendermail='prasanth@caratred.com',recivermail='bhanuchander008@gmail.com',subject='Hi',emailbody='test', htmlcontent=res, attach=None)

             #index("invoice","bhanuchander008@gmail.com","sucesss")
             return Response(render_template('byblosInvoice.html',order_data=order_data), mimetype='text/html', status=200)

        except Exception as e:
            return({"success":False,"message":str(e)})
