import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager


from db import db
from resources.items import blp as ItemBlueprint
from resources.stores import blp as StoreBlueprint
from resources.tags import blp as TagBlueprint
from resources.user import blp as UserBluePrint

from blocklist import BLOCKLIST

base_dir = os.path.abspath(os.path.dirname(__file__))

def create_app(db_url: str = None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Marketplace RestAPI"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(base_dir, "data.db"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_JWT_SECRET_KEY")
    
    db.init_app(app=app)

    api = Api(app=app)
    jwt = JWTManager(app=app)
    
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload): 
        return jwt_payload["jti"] in BLOCKLIST
    
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has been revoked.",
                "error": "token_revoked"
            }), 
            401
        )
    
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        pass
    
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has expired.",
                "error": "token_expired"
            }), 
            401
        )
    
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Signature verification failed.",
                "error": "invalid_token"
                }), 
            401
        )
    
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "message": "Request does not contain an access token.",
                "error": "authorization_required"
                }), 
            401
        )
    
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBluePrint)
    
    return app