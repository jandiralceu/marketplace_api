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
        return ItemModel.query.all()
    
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


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200)
    def put(self, body, id: str):
        item: ItemModel | None = ItemModel.query.get(id)
        if item:
            item.name = body["name"]
            item.price = body["price"]
        else:
            item = ItemModel(id=id, **body)
        
        db.session.add(item)
        db.session.commit()
        
        return item
    
    
    @blp.response(204)
    def delete(self, id: str):
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
