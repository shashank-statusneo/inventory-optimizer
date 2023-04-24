# Business logic for user

import uuid
import datetime
import logging

from modules.user import db
from modules.user.model import User
from typing import Dict, Tuple
from utils.exceptions import CustomException


logger = logging.getLogger("starter-kit")


def save_new_user(data):
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
        registered_on=datetime.datetime.utcnow(),
    )
    save_changes(new_user)

    response["data"] = {"id": new_user.id, "public_id": new_user.public_id}
    response["message"] = "User Registered Successfully"

    return response, 201


def get_all_users():
    """
    Get user details

    Returns:
        users (list): user details
    """

    users = User.query.all()
    return users


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            "status": "success",
            "message": "Successfully registered.",
            "Authorization": auth_token.decode(),
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
            "debug_messages": f"{e}",
        }
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()
