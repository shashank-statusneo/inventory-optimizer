"""
This file (test_models.py) contains the unit tests for the user/models.py file.
"""
from modules.user.model import User
import uuid


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated,
    and active fields are defined correctly
    """
    user = User(
        email="test_user_3@gmail.com",
        username="test_user_3",
        password="test_passwrord_3",
        public_id=str(uuid.uuid4()),
    )
    assert user.email == "test_user_3@gmail.com"
    assert user.password_hashed != "test_password_3"
    assert user.__repr__() == "<User: test_user_3@gmail.com>"
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.email == "test_user_4@gmail.com"
    assert new_user.password_hashed != "test_password_4"


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password("test_password_5")
    assert new_user.password_hashed != "test_password_5"
    assert new_user.is_password_correct("test_password_5")
    assert not new_user.is_password_correct("test_password_6")
    assert not new_user.is_password_correct("test_password_4")
