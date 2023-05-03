"""
This file (test_model.py) contains the unit
tests for the modules/users/model.py file.
"""
from modules.users.model import encode_auth_token, decode_auth_token

# import uuid


def test_new_user(test_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """

    assert test_user.email == "test_email@test.com"
    assert test_user.username == "test_username"
    assert test_user.password_hashed != "test_password"
    assert test_user.__repr__() == "<User: test_email@test.com>"
    assert test_user.is_authenticated
    assert test_user.is_active
    assert not test_user.is_anonymous


def test_user_id(test_user, test_client):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check if user id is valid or not
    """

    user_id = test_user.get_id()
    assert isinstance(user_id, str)


def test_encode_decode_auth_token(test_user, mocker):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check if the encoded auth_token is generated correctly
    """

    user_id = test_user.get_id()
    encoded_auth_token = encode_auth_token(user_id=user_id)
    assert isinstance(encoded_auth_token, str)

    wrong_encoded_auth_token = encode_auth_token(user_id=None)
    assert isinstance(wrong_encoded_auth_token, Exception)

    # m = mocker.patch("modules.users.model.Blacklist", return_value=False)
    m = mocker.patch(
        "modules.users.model.BlacklistToken.check_blacklist",
        return_value=True,
    )
    # decoded_user_id = decode_auth_token(auth_token=encoded_auth_token)
    decoded_user_id = decode_auth_token(auth_token=encoded_auth_token)

    m.assert_called_once_with(encoded_auth_token)

    assert isinstance(decoded_user_id, str)
    assert decoded_user_id == user_id


# def test_setting_password(new_user):
#     """
#     GIVEN an existing User
#     WHEN the password for the user is set
#     THEN check the password is stored correctly and not as plaintext
#     """
#     new_user.set_password("test_password_5")
#     assert new_user.password_hashed != "test_password_5"
#     assert new_user.is_password_correct("test_password_5")
#     assert not new_user.is_password_correct("test_password_6")
#     assert not new_user.is_password_correct("test_password_4")
