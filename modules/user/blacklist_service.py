from . import db

from modules.user.blacklist_model import BlacklistToken
from typing import Dict, Tuple
from utils.exceptions import DatabaseErrorException


def save_token(token: str) -> Tuple[Dict[str, str], int]:
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
    except Exception as e:
        raise DatabaseErrorException(
            debug_message="Failed to blacklist Authorization Token",
            error_message=f"Database Insertion Error: {e}",
        )
