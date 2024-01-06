import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schema import PlainStoreSchema

blp = Blueprint("stores", __name__, description="Operations on Stores table in database")


@blp.route("/stores")
class Store(MethodView):
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
class StoreById(MethodView):
    @blp.response(200, PlainStoreSchema)
    def get(self, id: str):
        try:
            pass
        except KeyError:
            pass
    
    @blp.response(204)
    def delete(self, id: str):
        try:
            pass
        except KeyError:
            pass
    
    @blp.arguments(PlainStoreSchema)
    @blp.response(200)
    def put(self, bod, id: str):
        try:
            pass
        except KeyError:
            pass