import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from db import db

from schema import PlainItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Items table in database")


@blp.route("/items")
class Item(MethodView):
    @blp.response(200, PlainItemSchema(many=True))
    def get(self):
        raise NotImplementedError("Get all stores is not implemented yet")
    
    @blp.arguments(PlainItemSchema)
    @blp.response(201, PlainItemSchema)
    def post(self, body):
        item = ItemModel(**body)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500, 
                message="The server encountered an unexpected condition that prevented it " +
                "from fulfilling the request."
            )
        return item
        
@blp.route("/items/<string:id>")
class ItemById(MethodView):
    @blp.response(200, PlainItemSchema)
    def get(self, id: str):
        return ItemModel.query.get_or_404(id)
    
    @blp.response(204)
    def delete(self, id: str):
        raise NotImplementedError("Get all stores is not implemented yet")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200)
    def put(self, body, id: str):
        raise NotImplementedError("Get all stores is not implemented yet")