# Store all db models for user

from . import db, flask_bcrypt
import datetime
from typing import Union
import jwt
from modules.user.config import Config
from modules.user.blacklist_model import BlacklistToken
from utils.exceptions import CustomException, AuthorizationException


class User(db.Model):
    """User Model for storing user related details"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=1, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        print(auth_token)
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                raise CustomException(
                    debug_message="Please log in again.",
                    http_code=403,
                    error_message="Authorization Token is blacklisted.",
                )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise CustomException(
                debug_message="Please log in again.",
                http_code=403,
                error_message="Signature expired.",
            )
        except jwt.InvalidTokenError:
            raise AuthorizationException(
                http_code=401,
                debug_message="Invalid Token",
                error_message="Please log in again.",
            )

    def __repr__(self):
        return "<User '{}'>".format(self.username)
