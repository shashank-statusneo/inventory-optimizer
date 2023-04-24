from flask_restx import Namespace, fields


class LoginSchema:
    api = Namespace("auth", description="Login related operations")
    user_auth = api.model(
        "auth_details",
        {
            "email": fields.String(
                required=True, description="email address"
            ),
            "password": fields.String(
                required=True, description="user password"
            ),
        },
    )
