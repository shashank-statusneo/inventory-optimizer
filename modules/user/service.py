# Business logic for user

import logging
import uuid
from typing import Dict

from utils.exceptions import (
    AuthorizationException,
    CustomException,
    DatabaseErrorException,
    ResourceDoesNotExistException,
)

from modules import db
from modules.user.model import BlacklistToken, User

logger = logging.getLogger("starter-kit")


def save_new_user(data: Dict[str, str]):
    """
    Creates a new user

    Args:
        data (dict):
            email (str): user email
            username(str): user name
            password (str): user password

    Returns:
        id (int): new user id
        public_id (str): new user public id
    """

    logger.info("in save_new_user")

    response = {"success": True, "data": []}

    user = User.query.filter_by(email=data["email"]).first()

    if user:
        raise CustomException(
            http_code=409,
            debug_message="User already exists with this email id",
            error_message="User creation failed",
        )

    user = User.query.filter_by(username=data["username"]).first()

    if user:
        raise CustomException(
            http_code=409,
            debug_message="User already exists with this username",
            error_message="User creation failed",
        )

    new_user = User(
        public_id=str(uuid.uuid4()),
        email=data["email"],
        username=data["username"],
        password=data["password"],
    )
    save_changes(new_user)
    auth_token = new_user.encode_auth_token(new_user.id)

    response["data"] = {
        "id": new_user.id,
        "public_id": new_user.public_id,
        "auth_token": auth_token,
    }
    response["message"] = "User Registered Successfully"

    return response, 201


def get_user_data(data: Dict[str, str]):
    """_summary_

    Args:
        data (Dict[str, str]): _description_
    """

    logger.info("in get_user_data")

    response = {"success": True, "data": []}

    auth_token = data.get("Authorization")

    if not auth_token:
        raise AuthorizationException(
            http_code=401,
            debug_message="Please provide a valid authorization token",
            error_message="User get status failed",
        )

    decode_response = User.decode_auth_token(auth_token)

    if isinstance(decode_response, str):
        raise CustomException(
            http_code=401,
            debug_message=decode_response,
            error_message="User get status failed",
        )

    user = User.query.filter_by(id=decode_response).first()

    response["data"] = {
        "user_id": user.id,
        "email": user.email,
        "registered_on": str(user.registered_on),
    }

    return response, 200


def login_existing_user(data: Dict[str, str]):
    """_summary_

    Args:
        data (Dict[str, str]): _description_

    Raises:
        ResourceDoesNotExistException: _description_
        AuthorizationException: _description_
    """

    logger.info("in login_existing_user")

    response = {"success": True, "data": []}

    # fetch the user data
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not user.id:
        raise ResourceDoesNotExistException(
            resource_name="user", resource_id=data.get("email")
        )

    if not user.is_password_correct(data.get("password")):
        raise AuthorizationException(
            http_code=401,
            debug_message="Invalid Email or Password",
            error_message="User Login Failed",
        )

    auth_token = user.encode_auth_token(user.id)
    response["data"] = {"auth_token": auth_token}

    response["message"] = "User Successfully Logged In"
    return response, 200


def logout_existing_user(data: Dict[str, str]):
    """_summary_

    Args:
        data (Dict[str, str]): _description_
    """

    logger.info("in logout_existing_user")

    response = {"success": True, "data": []}

    auth_token = data.get("Authorization")

    if not auth_token:
        raise AuthorizationException(
            http_code=401,
            debug_message="Please provide a valid authorization token",
            error_message="User get status failed",
        )

    decode_response = User.decode_auth_token(auth_token)

    if isinstance(decode_response, str):
        raise CustomException(
            http_code=401,
            debug_message=decode_response,
            error_message="User get status failed",
        )

    # Blacklist Token
    blacklist_token = BlacklistToken(token=auth_token)
    save_changes(blacklist_token)

    response["message"] = "User Successfully Logged out"
    return response, 200


def get_logged_in_user(data: Dict[str, str]):
    """_summary_

    Args:
        data (Dict[str, str]): _description_

    Returns:
        _type_: _description_
    """

    logger.info("in get_logged_in_user")

    response = {"success": True, "data": []}

    auth_token = data.headers.get("Authorization")

    if not auth_token:
        raise AuthorizationException(
            http_code=401,
            debug_message="Please provide a valid authorization token",
            error_message="User get status failed",
        )

    decode_response = User.decode_auth_token(auth_token)

    if isinstance(decode_response, str):
        raise CustomException(
            http_code=401,
            debug_message=decode_response,
            error_message="User get status failed",
        )

    user = User.query.filter_by(id=decode_response).first()
    response["data"] = (
        {
            "user_id": user.id,
            "email": user.email,
            "registered_on": str(user.registered_on),
        },
    )

    return response, 200


def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        raise DatabaseErrorException(
            debug_message=f"{e}", error_message="Databse Error Occured"
        )
