# Register all app routes

from flask_restx import Api
from flask import Blueprint

from modules.users.controller import (
    user_api as user_namespace,
    login_api as login_namespace,
    logout_api as logout_namespace,
)

from modules.orders.controller import order_api as order_namespace
from modules.inventory_optimizer.controller import demand_forecast_api as demand_forecast_namespace
from modules.inventory_optimizer.controller import vendor_api as vendor_namespace


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

api.add_namespace(demand_forecast_namespace)

api.add_namespace(vendor_namespace)
