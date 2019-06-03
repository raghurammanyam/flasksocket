from config import db,ma
from models.deliveryzonesmodel import Deliveryzones
from marshmallow.fields import Nested
#from schemas.address_schema import AddressGetSchema


class DeliveryzoneSchema(ma.ModelSchema):
    class Meta:
        model = Deliveryzones
        sqla_session = db.session


class DeliveryzoneGetSchema(ma.ModelSchema):
    class Meta:
        model = Deliveryzones
        sqla_session = db.session
