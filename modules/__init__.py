import os
import traceback
from json import dumps

from click import echo
from config import config_by_name
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from utils.exceptions import APIException
from werkzeug.exceptions import HTTPException

from flask_migrate import Migrate, init, migrate, upgrade, stamp


# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions (flask-sqlalchemy etc.) in
# the global scope, but without any arguments passed in.
# These instances are not attached to the application at this point.


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
# TODO: configure flask migrate
migrate_extension = Migrate()


# ----------------------------
# Application Factory Function
# ----------------------------


def create_app(env):
    """_summary_

    Args:
        env (str, optional): App Environment. Defaults to "dev".

    Returns:
        flask instance: Returns a flask app
    """
    # get app config from env

    config = config_by_name[env]
    print(config)

    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Configure the Flask Application
    app.config.from_object(config)

    # Add Exception Handlers
    register_error_handlers(app)

    #  Add CLI commamnds
    register_cli_commands(app)

    # Add flask extenstions
    initialize_extensions(app)

    with app.app_context():
        # run migration

        run_db_migration()

    return app


# ----------------
# Helper Functions
# ----------------


def run_db_migration():
    init(multidb=True)
    migrate()
    upgrade()


def register_error_handlers(app):
    # Since the application instance is now created, register each
    # Error Handler with the Flask application instance (app)

    @app.errorhandler(APIException)
    def handle_custom_exception(error):
        """Return a custom message and 400 status code"""

        response = {
            "success": False,
            "data": [],
            "error_code": error.starter_kit_code,
            "error_message": error.message,
            "debug_message": error.debug_message,
        }

        return response, error.http_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = err.get_response()
        # replace the body with JSON
        response.content_type = "application/json"
        response.data = dumps(
            {
                "success": False,
                "data": [],
                "error": err.name,
                "debug_message": err.description,
            }
        )

        return response

    @app.errorhandler(Exception)
    def internal_error(error):
        """runs if any code level error has occured"""

        # send proper error message rather than html broken response
        trace_err = traceback.format_exc()

        response = {
            "success": False,
            "data": [],
            "error": "Internal Server Error",
            "debug_message": str(error),
            "traceback": trace_err,
        }
        return response, 500


def register_cli_commands(app):
    @app.cli.command("init_db")
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo("Initialized the database!")


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)

    db.init_app(app)
    migrate_extension.init_app(app, db)
    flask_bcrypt.init_app(app)
    CORS(app)


# def check_db_initialization():
#     """_summary_

#     Args:
#         app (_type_): _description_
#     """
#     # Check if the database needs to be initialized

#     engines = db.engines

#     user_engine = engines.get("user")
#     app_meta_engine = engines.get("app_meta")

#     user_inspector = db.inspect(user_engine)
#     user_tables = user_inspector.get_table_names()

#     if ["users", "blacklist_tokens"] not in user_tables:
#         db.drop_all(bind_key="user")
#         db.create_all(bind_key="user")

#     app_meta_inspector = db.inspect(app_meta_engine)
#     app_meta_tables = app_meta_inspector.get_table_names()

#     if ["orders"] not in app_meta_tables:
#         db.drop_all(bind_key="app_meta")
#         db.create_all(bind_key="app_meta")
