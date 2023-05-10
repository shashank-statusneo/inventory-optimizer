import click
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

    return app


# ----------------
# Helper Functions
# ----------------


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
    def initialize_db():
        """Initializing database migrations."""
        echo("Initializing database migrations!")
        init(multidb=True)

    @app.cli.command("migrate_db")
    @click.option(
        "--db",
        required=True,
        type=click.Choice(["app_auth", "app_meta"], case_sensitive=True),
        help="Name of database that has to be migrated",
    )
    @click.option(
        "--m",
        required=True,
        type=str,
        help="Migration message",
    )
    def migrate_db(db, m):
        """Prepare database migration scripts."""
        echo("Preparing database migration scripts!")
        stamp(tag=db)
        migrate(message=m, x_arg=db)

    @app.cli.command("upgrade_db")
    @click.option(
        "--db",
        required=True,
        type=click.Choice(["app_auth", "app_meta"], case_sensitive=True),
        help="Name of database that has to be migrated",
    )
    def upgrade_db(db):
        """Upgrading database migrations."""
        echo("Upgrading database migrations!")
        upgrade(x_arg=db)


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)

    db.init_app(app)
    migrate_extension.init_app(app, db)
    flask_bcrypt.init_app(app)
    CORS(app)
