import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schema import PlainItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Items table in database")


@blp.route("/items")
class Item(MethodView):
    @blp.response(200, PlainItemSchema(many=True))
    def get(self):
        try:
            pass
        except KeyError:
            pass
    
    @blp.arguments(PlainItemSchema)
    @blp.response(201, PlainItemSchema)
    def post(self, body):
        try:
            pass
        except KeyError:
            pass
        
@blp.route("/items/<string:id>")
class ItemById(MethodView):
    @blp.response(200, PlainItemSchema)
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
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200)
    def put(self, body, id: str):
        try:
            pass
        except KeyError:
            pass