# Register all app routes

from flask_restx import Api
from flask import Blueprint

from modules.users.controller import (
    user_api as user_namespace,
    login_api as login_namespace,
    logout_api as logout_namespace,
)

from modules.orders.controller import order_api as order_namespace


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

api.add_namespace(logout_namespace)

api.add_namespace(order_namespace)
