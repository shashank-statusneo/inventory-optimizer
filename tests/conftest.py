# Define fixture her to make a fixture available to multiple test files

from pytest import fixture

import os
from app import app
from config import config_by_name


@fixture()
def create_new_app():
    ENV = os.getenv("FLASK_ENV") or "dev"
    app.config.from_object(config_by_name[ENV])
    return app
