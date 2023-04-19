from modules.user.model import User
from modules.user.blacklist_service import save_token
from typing import Dict, Tuple
import logging
from utils.exceptions import (
    ResourceDoesNotExistException,
    AuthorizationException,
    CustomException,
)

logger = logging.getLogger("starter-kit")


class Auth:
    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        """
        Login a user

        args:
            data: Dict

        returns:
            auth_token: str
        """

        logger.info("in login_user")

        response = {"success": True, "data": []}

        # fetch the user data
        user = User.query.filter_by(email=data.get("email")).first()

        if not user or not user.id:
            raise ResourceDoesNotExistException(
                resource_name="user", resource_id=data.get("email")
            )

        if not user.check_password(data.get("password")):
            raise AuthorizationException(
                http_code=401,
                debug_message="Invalid Email or Password",
                error_message="User Login Failed",
            )

        auth_token = User.encode_auth_token(user.id)

        response["data"] = {"Authorization": auth_token}
        response["message"] = "User Successfully Logged In"

        return response, 200

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        """
        Logout a user

        args:
            data: str

        returns:
            auth_token: str
        """

        logger.info("in logout_user")

        response = {"success": True, "data": []}

        if not data:
            raise CustomException(
                debug_message="Please Provide a valid Authorization token",
                error_message="User Logout Failed",
                http_code=403,
            )

        _ = User.decode_auth_token(data)
        # mark the token as blacklisted
        save_token(token=data)

        response["message"] = "User Successfully Logged Out"
        return response, 200

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get("Authorization")
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "email": user.email,
                        "admin": user.admin,
                        "registered_on": str(user.registered_on),
                    },
                }
                return response_object, 200
            response_object = {"status": "fail", "message": resp}
            return response_object, 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return response_object, 401
