import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import StoreModel
from db import db

from schema import PlainStoreSchema

blp = Blueprint("stores", __name__, description="Operations on Stores table in database")


@blp.route("/stores")
class Store(MethodView):
    @blp.response(200, PlainStoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(PlainStoreSchema)
    @blp.response(201, PlainStoreSchema)
    def post(self, body):
        item = StoreModel(**body)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(
                400, 
                message="A Store with that name already exists."
            )
        except SQLAlchemyError:
            abort(
                500, 
                message="The server encountered an unexpected condition that prevented it " +
                "from fulfilling the request."
            )
        return item
        
@blp.route("/stores/<string:id>")
class StoreById(MethodView):
    @blp.response(200, PlainStoreSchema)
    def get(self, id: str):
        return StoreModel.query.get_or_404(id)
    
    
    @blp.arguments(PlainStoreSchema)
    @blp.response(200)
    def put(self, bod, id: str):
        store = StoreModel.query.get_or_404(id)
        raise NotImplementedError("Delete store is not implemented yet")

        
        
    @blp.response(204)
    def delete(self, id: str):
        store = StoreModel.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()