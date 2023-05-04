import datetime

from flask import current_app as app
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode

from modules import db, flask_bcrypt


class Users(db.Model):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * id: database id of the user
        * email - email address of the user
        * registered_on - date & time that the user registered
        * public_id: public id of the user
        * username: name of the user
        * password_hashed - hashed password (using flask bcrypt)


    REMEMBER: Never store the plaintext password in a database!
    """

    __tablename__ = "users"

    # __bind_key__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(60), unique=True)
    password_hashed = db.Column(db.String(100))

    def __init__(
        self,
        email: str,
        username: str,
        public_id: str,
        password: str,
    ):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.email = email
        self.username = username
        self.public_id = public_id
        self.password_hashed = flask_bcrypt.generate_password_hash(
            password
        ).decode("utf-8")
        self.registered_on = datetime.datetime.utcnow()

    # @staticmethod
    # def encode_auth_token(user_id):
    #     """
    #     Generates the Auth Token
    #     :return: string
    #     """
    #     try:
    #         payload = {
    #             "exp": datetime.datetime.utcnow()
    #             + datetime.timedelta(days=0, seconds=3600),
    #             "iat": datetime.datetime.utcnow(),
    #             "sub": user_id,
    #         }
    #         return encode(
    #             payload, app.config.get("SECRET_KEY"), algorithm="HS256"
    #         )
    #     except Exception as e:
    #         return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = decode(
                auth_token, app.config.get("SECRET_KEY"), algorithms="HS256"
            )
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            return payload["sub"]
        except ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except InvalidTokenError:
            return "Invalid token. Please log in again."

    def is_password_correct(self, password: str):
        return flask_bcrypt.check_password_hash(self.password_hashed, password)

    def set_password(self, password: str):
        self.password_hashed = self._generate_password_hash(password)

    @staticmethod
    def _generate_password_hash(password):
        return flask_bcrypt.generate_password_hash(password).decode("utf-8")

    def __repr__(self):
        return f"<User: {self.email}>"

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = "blacklist_tokens"

    # __bind_key__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return "<id: token: {}".format(self.token)


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        if not user_id:
            raise Exception
        payload = {
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(days=0, seconds=3600),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256")
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = decode(
            auth_token, app.config.get("SECRET_KEY"), algorithms="HS256"
        )
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            return "Token blacklisted. Please log in again."
        return payload["sub"]
    except ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except InvalidTokenError:
        return "Invalid token. Please log in again."
