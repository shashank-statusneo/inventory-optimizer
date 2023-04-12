import os

host = "sql12.freemysqlhosting.net"
username = "sql12612529"
password = "TZuKC2mhtc"
port = 3306
database = "sql12612529"

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_9870")
    DEBUG = os.getenv("DEBUG", False)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{username}:{password}@{host}:{port}/{database}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{username}:{password}@{host}:{port}/{database}"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)

key = Config.SECRET_KEY
