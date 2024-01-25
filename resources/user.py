from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import UserModel
from schema import UserSchema

blp = Blueprint("users", __name__, description="Operations on user")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(204)
    def post(self, body):
        try:
            user = UserModel(
                username=body["username"],
                password=pbkdf2_sha256.hash(body["password"])
            )
            
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(
                400, 
                message="A User with that name already exists."
            )
        except SQLAlchemyError:
            abort(
                500, 
                message="The server encountered an unexpected condition that prevented it " +
                "from fulfilling the request."
            )


@blp.route("/users/<int:id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, id):
        return UserModel.query.get_or_404(id)
    
    @blp.response(204)
    def delete(self, id):
        user = UserModel.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()