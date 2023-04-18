# Register all app routes

from flask_restx import Api
from flask import Blueprint

from modules.user.controller import api as user_namespace
from modules.login.controller import api as login_namespace

blueprint = Blueprint("api", __name__)
authorizations = {
    "apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    blueprint,
    title="StarterKit",
    version="1.0.0",
    description="Login Service",
    authorizations=authorizations,
    security="apiKey",
)

api.add_namespace(user_namespace, path="/user")

api.add_namespace(login_namespace)
