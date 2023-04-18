# Store business logic for user

import uuid
import datetime

from modules.user import db
from modules.user.model import User
from typing import Dict, Tuple


def save_new_user(data):
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data["email"],
            username=data["username"],
            password=data["password"],
            registered_on=datetime.datetime.utcnow(),
        )
        save_changes(new_user)
        response_object = {
            "success": True,
            "message": "User Registered Successfully.",
        }
        return response_object, 201
    else:
        response_object = {
            "success": False,
            "message": "User already exists. Please Log in.",
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


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
