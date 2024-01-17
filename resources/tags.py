from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import TagModel, StoreModel
from db import db

from schema import TagSchema

blp = Blueprint("tags", __name__, description="Operations on Tags table in database")


@blp.route("/stores/<string:store_id>/tags")
class StoreById(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)
        
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, body, store_id):
        try:
            if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == body["name"]).first():
                abort(400, message="A tag with same name already exists in that store.")
                
            tag = TagModel(**body, store_id=store_id)
            
            db.session.add(tag)
            db.session.commit()
            
            return tag
        except SQLAlchemyError as err:
            abort(
                500, 
                message=str(err)
            )