import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        try:
            pass
        except KeyError:
            pass
    
    def post(self):
        try:
            pass
        except KeyError:
            pass
        
@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id: str):
        try:
            pass
        except KeyError:
            pass
    
    def delete(self, store_id: str):
        try:
            pass
        except KeyError:
            pass
        
    def put(self):
        try:
            pass
        except KeyError:
            pass