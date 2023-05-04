"""
This file (test_users.py) contains the functional tests for the `users`.
These tests use GETs and POSTs to different URLs to check
for the proper behavior of the `users` blueprint.
"""

import pytest
from json import loads


class TestUserRoutes:
    @pytest.mark.user
    def test_new_user(self, client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/user' route is requested (POST)
        THEN check the response is valid

        """
        response = client.post(
            path="/user/",
            json={
                "email": "test_user_1@gmail.com",
                "username": "test_user_1",
                "password": "test_password_1",
            },
        )

        assert response.status_code == 201

    @pytest.mark.user
    def test_get_user_data(self, client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/user' route is requested (GET)
        THEN check the response is valid

        """
        response = client.post(
            path="/user/",
            json={
                "email": "test_user@gmail.com",
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == 201

        res = loads(response.data)
        res_data = res.get("data")
        auth_token = res_data.get("auth_token")

        # check validity of auth_token
        assert isinstance(auth_token, str)

        response = client.get(
            path="/user/",
            headers={"Authorization": auth_token},
        )

        assert response.status_code == 200
        res = loads(response.data)
        res_data = res.get("data")
        email = res_data.get("email")

        assert email == "test_user@gmail.com"

    @pytest.mark.user
    def test_valid_login_logout(self, client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/login' route is requested to (POST)
        THEN check the response is valid
        """
        response = client.post(
            "/login/",
            json={
                "email": "test_user_1@gmail.com",
                "password": "test_password_1",
            },
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200
        res = loads(response.data)
        res_data = res.get("data")
        auth_token = res_data.get("auth_token")

        # check validity of auth_token
        assert isinstance(auth_token, str)

        """
        GIVEN a Flask application configured for testing
        WHEN the '/logout' route is requested (POST)
        THEN check the response is valid
        """
        response = client.post(
            "/logout/",
            headers={"Authorization": auth_token},
        )
        assert response.status_code == 200

    @pytest.mark.user
    def test_invalid_login(self, client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/login' route is requested to with invalid credentials (POST)
        THEN check an error message is returned to the user
        """
        response = client.post(
            "/login/",
            json={
                "email": "test_user_1@gmail.com",
                "password": "test_password_0",
            },
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 401
