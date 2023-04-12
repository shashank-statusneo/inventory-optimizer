# Routes for login

from flask import request
from flask_restx import Resource

from modules.login.schema import LoginSchema
from modules.login.service import Auth

api = LoginSchema.api
user_auth = LoginSchema.user_auth


@api.route("/login")
class UserLogin(Resource):
    """
    User Login Resource
    """

    @api.doc("user login")
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)
