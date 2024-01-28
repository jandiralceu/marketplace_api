from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity

from models import UserModel
from schema import UserSchema
from blocklist import BLOCKLIST


blp = Blueprint("auth", __name__, description="Auth operations")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, body):
        user = UserModel.query.filter(UserModel.username == body["username"]).first()
        
        if user and pbkdf2_sha256.verify(body["password"], user.password):
            return {
                "access_token": create_access_token(identity=user.id, fresh=True),
                "refresh_token": create_refresh_token(identity=user.id)
            }
        
        abort(401, message="Invalid Credentials. Verify your username or password")


@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        
        return {
            "access_token": create_access_token(identity=current_user, fresh=False)
        }


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @blp.response(204)
    def post(self):
        jti = get_jwt()["jti"]
        # Use redis to persist revoked tokens
        BLOCKLIST.add(jti)
