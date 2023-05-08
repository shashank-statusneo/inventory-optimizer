import os

import yaml
from yaml.loader import SafeLoader

basedir = os.path.abspath(os.path.dirname(__file__))
ENV = os.getenv("FLASK_ENV") or "dev"

with open(os.path.join(basedir, ENV + ".yaml")) as config_file:
    config = yaml.load(config_file, Loader=SafeLoader)


class Config(object):
    DEBUG = config.get("DEBUG")
    SECRET_KEY = config.get("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = config.get("PROPAGATE_EXCEPTIONS")

    # Database Config
    SQLALCHEMY_TRACK_MODIFICATIONS = config.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    )

    databases = config.get("DATABASE")

    app_auth_db = databases.get("app_auth")

    type = app_auth_db.get("type", "mysql")
    username = app_auth_db.get("username", "root")
    password = app_auth_db.get("password", "")
    host = app_auth_db.get("host", "localhost")
    port = app_auth_db.get("port", 3306)
    database = app_auth_db.get("database", "")

    SQLALCHEMY_DATABASE_URI = (
        f"{type}://{username}:{password}@{host}:{port}/{database}"
    )

    binds_database = databases.get("binds")
    if binds_database:
        SQLALCHEMY_BINDS = {}

        for key, value in binds_database.items():
            type = value.get("type", "mysql")
            username = value.get("username", "root")
            password = value.get("password", "")
            host = value.get("host", "localhost")
            port = value.get("port", 3306)
            database = value.get("database", "")
            SQLALCHEMY_BINDS[
                key
            ] = f"{type}://{username}:{password}@{host}:{port}/{database}"

    print(SQLALCHEMY_BINDS)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)
