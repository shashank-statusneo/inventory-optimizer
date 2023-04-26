import logging

from flask import request
from flask_restx import Resource

from modules.user.schema import LoginSchema, LogoutSchema, UserSchema
from modules.user.service import (
    get_user_data,
    login_existing_user,
    logout_existing_user,
    save_new_user,
)

user_api = UserSchema.api
user_schema = UserSchema.schema

login_api = LoginSchema.api
login_schema = LoginSchema.schema

logout_api = LogoutSchema.api

logger = logging.getLogger("starter-kit")


@user_api.route("/")
class User(Resource):
    """
    Args:
        Resource (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        logger.info("in user main class init")
        super().__init__(*args, **kwargs)

    @user_api.expect(user_schema, validate=True)
    def post(self):
        """_summary_"""

        logger.info("in User module post")

        request_data = request.json
        return save_new_user(request_data)

    @user_api.expect()
    def get(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        logger.info("in User module get")

        request_headers = request.headers
        return get_user_data(request_headers)


@login_api.route("/")
class Login(Resource):
    """
    Args:
        Resource (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        logger.info("in login main class init")
        super().__init__(*args, **kwargs)

    def post(self):
        """_summary_"""

        logger.info("in Login module post")

        request_data = request.json
        return login_existing_user(data=request_data)


@logout_api.route("/")
class Logout(Resource):
    """
    Args:
        Resource (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        logger.info("in Logout main class init")
        super().__init__(*args, **kwargs)

    def post(self):
        """_summary_"""

        logger.info("in Logout module post")

        request_headers = request.headers
        return logout_existing_user(request_headers)
