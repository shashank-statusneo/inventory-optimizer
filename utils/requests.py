# Store request helper functions

from functools import wraps
from typing import Callable

from flask import request
from modules.user.service import get_logged_in_user


def token_required(f) -> Callable:
    """_summary_

    Args:
        f (_type_): _description_

    Returns:
        Callable: _description_
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        response, status = get_logged_in_user(request)
        user_id = response.get("data", {}).get("user_id")

        if not user_id:
            return response, status

        return f(*args, **kwargs)

    return decorated
