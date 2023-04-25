# Define fixture her to make a fixture available to multiple test files

from pytest import fixture

import os
from app import app
from config import config_by_name
import requests
from json import dumps


@fixture(scope="session")
def create_new_app():
    ENV = os.getenv("FLASK_ENV") or "dev"
    app.config.from_object(config_by_name[ENV])
    return app


@fixture
def register_new_user():
    request_response = requests.post(
        "http://127.0.0.1:5000/starter-kit/user",
        data=dumps(
            {
                "email": "new_user_1@gmail.com",
                "password": "pswd123",
            }
        ),
        content_type="application/json",
    )
    return request_response
