from flask_restx import Namespace, fields


class LoginSchema:
    api = Namespace("Login", description="Login related operations")
    user_auth = api.model(
        "auth_details",
        {
            "email": fields.String(
                required=True, description="The email address"
            ),
            "password": fields.String(
                required=True, description="The user password"
            ),
        },
    )
