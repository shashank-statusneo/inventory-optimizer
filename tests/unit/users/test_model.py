"""
This file (test_model.py) contains the unit
tests for the modules/users/model.py file.
"""
from modules.users.model import Users, encode_auth_token, decode_auth_token
import pytest


@pytest.mark.usefixtures("import_users")
class TestUser:
    """User Tests"""

    @pytest.mark.user_model
    def test_user_data(self):
        """
        GIVEN
        WHEN
        THEN
        """
        user = Users.query.filter_by(email="test_1@test.com").first()

        assert user.username == "test_1"
        assert user.password_hashed != "password_1"
        assert user.__repr__() == "<User: test_1@test.com>"
        assert user.is_authenticated
        assert user.is_active
        assert not user.is_anonymous

        total_users = Users.query.count()
        assert total_users == 3

    @pytest.mark.user_model
    def test_new_user(self, test_user):
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

    @pytest.mark.user_model
    def test_user_id(self, test_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check if user id is valid or not
        """

        user_id = test_user.get_id()
        assert isinstance(user_id, str)

    @pytest.mark.user_model
    def test_encode_decode_auth_token(self, test_user, mocker):
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

        m = mocker.patch(
            "modules.users.model.BlacklistToken.check_blacklist",
            side_effect=[False, True],
        )
        decoded_user_id = decode_auth_token(auth_token=encoded_auth_token)
        error_decoded_user_id = decode_auth_token(
            auth_token=encoded_auth_token
        )

        m.assert_called_with(encoded_auth_token)

        assert isinstance(decoded_user_id, str)
        assert decoded_user_id == user_id

        assert isinstance(decoded_user_id, str)
        assert error_decoded_user_id != user_id
