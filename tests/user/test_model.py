# User Module Database Tests


from pytest import mark
from modules.user.model import User
import datetime
from modules.user import db


@mark.user
def test_create_new_user():
    """Testing
    Create a new user

    Args:
        create_new_app (_type_): _description_
    """
    user = User(
        email="shashank7@gmail.com",
        username="shashank7",
        password="test",
        registered_on=datetime.datetime.utcnow(),
    )
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, str)
