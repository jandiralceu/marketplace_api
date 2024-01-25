from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db

from models import TagModel, StoreModel, ItemModel
from schema import TagSchema, TagAndItemSchema

blp = Blueprint("tags", __name__, description="Operations on Tags table in database")


@blp.route("/stores/<string:store_id>/tags")
class TagsInStore(MethodView):
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


@blp.route("/items/<string:item_id>/tags/<string:tag_id>")
class linkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
            
            item.tags.append(tag)
            
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(
                500, 
                message=str(err)
            )
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
            
            item.tags.remove(tag)
            
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(
                500, 
                message=str(err)
            )
        except:
            abort(
                500, 
                message=str(err)
            )


@blp.route("/tags/<string:id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
        return TagModel.query.get_or_404(id)
    
    
    @blp.response(200, description="Deletes a tag if no item is linked with it")
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400, description="There is linked items into this tag")
    def delete(self, id):
        tag = TagModel.query.get_or_404(id)
            
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()    
            return
        
        abort(404, message="Tag not found")
        