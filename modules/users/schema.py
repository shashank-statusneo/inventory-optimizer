#  Store api data transfer models


from flask_restx import Namespace, fields


class UserSchema:
    api = Namespace("user", description="User operations")
    schema = api.model(
        "user",
        {
            "email": fields.String(
                required=True, description="user email address"
            ),
            "username": fields.String(
                required=True, description="user username"
            ),
            "password": fields.String(
                required=True, description="user password"
            ),
            "public_id": fields.String(description="user Identifier"),
        },
    )


class LoginSchema:
    api = Namespace("login", description="Login operations")
    schema = api.model(
        "login",
        {
            "email": fields.String(required=True, description="email address"),
            "password": fields.String(
                required=True, description="user password"
            ),
        },
    )


class LogoutSchema:
    api = Namespace("logout", description="Logout operations")
