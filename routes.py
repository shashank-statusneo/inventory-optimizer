# Register all app routes

from flask_restx import Api
from flask import Blueprint

from modules.user.controller import api as user_namespace
from modules.login.controller import api as login_namespace

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint, title="StarterKit", version="1.0.0", description="Login Service"
)

api.add_namespace(user_namespace, path="/user")

api.add_namespace(login_namespace, path="/login")
