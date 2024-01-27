from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from db import db
from models import UserModel
from schema import UserSchema
from blocklist import BLOCKLIST


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



@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, body):
        user = UserModel.query.filter(UserModel.username == body["username"]).first()
        
        if user and pbkdf2_sha256.verify(body["password"], user.password):
            return {"token": create_access_token(identity=user.id)}
        
        abort(401, message="Invalid Credentials. Verify your username or password")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @blp.response(204)
    def post(self):
        jti = get_jwt()["jti"]
        # Use redis to persist revoked tokens
        BLOCKLIST.add(jti)


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