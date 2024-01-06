import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schema import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        try:
            pass
        except KeyError:
            pass
    
    @blp.arguments(StoreSchema)
    def post(self, body):
        try:
            pass
        except KeyError:
            pass
        
@blp.route("/stores/<string:id>")
class Store(MethodView):
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
    
    @blp.arguments(StoreSchema)
    def put(self, bod, id: str):
        try:
            pass
        except KeyError:
            pass