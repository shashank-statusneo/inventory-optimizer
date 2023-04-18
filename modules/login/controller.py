from flask import request
from flask_restx import Resource
import logging

from modules.login.service import Auth
from modules.login.schema import LoginSchema
from typing import Dict, Tuple

api = LoginSchema.api
user_auth = LoginSchema.user_auth


logger = logging.getLogger("starter-kit")


@api.route("/login")
class UserLogin(Resource):
    """
    User Login Resource
    """

    @api.doc("user login")
    @api.expect(user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route("/logout")
class LogoutAPI(Resource):
    """
    User Logout Resource
    """

    @api.doc("logout a user")
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        auth_header = request.headers.get("Authorization")
        return Auth.logout_user(data=auth_header)
