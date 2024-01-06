import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schema import PlainStoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, PlainStoreSchema(many=True))
    def get(self):
        try:
            pass
        except KeyError:
            pass
    
    @blp.arguments(PlainStoreSchema)
    @blp.response(201, PlainStoreSchema)
    def post(self, body):
        try:
            pass
        except KeyError:
            pass
        
@blp.route("/stores/<string:id>")
class Store(MethodView):
    @blp.response(200, PlainStoreSchema)
    def get(self, id: str):
        try:
            pass
        except KeyError:
            pass
    
    def delete(self, id: str):
        try:
            pass
        except KeyError:
            pass
    
    @blp.arguments(PlainStoreSchema)
    def put(self, bod, id: str):
        try:
            pass
        except KeyError:
            pass