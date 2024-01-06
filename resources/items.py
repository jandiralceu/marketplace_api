import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schema import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/items")
class Store(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            pass
        except KeyError:
            pass
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, body):
        try:
            pass
        except KeyError:
            pass
        
@blp.route("/items/<string:id>")
class StoreWithID(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id: str):
        try:
            pass
        except KeyError:
            pass
    
    def delete(self, item_id: str):
        try:
            pass
        except KeyError:
            pass
    
    @blp.arguments(ItemUpdateSchema)
    def put(self, body, id: str):
        try:
            pass
        except KeyError:
            pass