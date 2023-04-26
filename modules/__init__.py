import os
import traceback
from json import dumps

import sqlalchemy as sa
from click import echo
from config import config_by_name
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from utils.exceptions import APIException
from werkzeug.exceptions import HTTPException

# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions (flask-sqlalchemy etc.) in
# the global scope, but without any arguments passed in.
# These instances are not attached to the application at this point.


db = SQLAlchemy()
flask_bcrypt = Bcrypt()


# ----------------------------
# Application Factory Function
# ----------------------------


def create_app(env="dev"):
    # get app config from env

    ENV = os.getenv("FLASK_ENV") or env

    config = config_by_name[ENV]

    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask Application
    app.config.from_object(config)

    initialize_extensions(app)
    register_error_handlers(app)
    register_cli_commands(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user") or not inspector.has_table(
        "blacklist_tokens"
    ):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized the database!")
    else:
        app.logger.info("Database already contains the user table.")

    return app


# ----------------
# Helper Functions
# ----------------


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    flask_bcrypt.init_app(app)
    CORS(app)


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
