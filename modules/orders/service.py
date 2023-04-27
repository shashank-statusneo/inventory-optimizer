# Business logic for order

import logging

from typing import Dict

from utils.exceptions import (
    DatabaseErrorException,
)

from modules import db
from modules.orders.model import Orders

logger = logging.getLogger("starter-kit")


def create_new_order(data: Dict[str, str]):
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

    new_order = Orders(
        user_id=data["user_id"],
        amount=data["amount"],
    )
    save_changes(new_order)

    response["data"] = {
        "id": new_order.id,
    }
    response["message"] = "Order Created Successfully"

    return response, 201


def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        raise DatabaseErrorException(
            debug_message=f"{e}", error_message="Databse Error Occured"
        )
