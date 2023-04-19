import os
import yaml
from yaml.loader import SafeLoader

basedir = os.path.abspath(os.path.dirname(__file__))
ENV = os.getenv("FLASK_ENV") or "dev"

with open(os.path.join(basedir, ENV + ".yaml")) as config_file:
    config = yaml.load(config_file, Loader=SafeLoader)


class DevelopmentConfig:

    # App config
    DEBUG = config.get("DEBUG")
    SECRET_KEY = config.get("SECRET_KEY")

    # Database Config
    SQLALCHEMY_TRACK_MODIFICATIONS = config.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    )
    SQLALCHEMY_BINDS = {}
    databases = config.get("DATABASE")
    for key, value in databases.items():
        type = value.get("type", "mysql")
        username = value.get("username", "root")
        password = value.get("password", "")
        host = value.get("host", "localhost")
        port = value.get("port", 3306)
        database = value.get("database", "")
        SQLALCHEMY_BINDS[
            key
        ] = f"mysql://{username}:{password}@{host}:{port}/{database}"


class TestingConfig:
    DEBUG = True


class ProductionConfig:
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)
