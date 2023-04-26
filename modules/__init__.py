import sqlalchemy as sa
from click import echo
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

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


def create_app(config):
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask Application
    app.config.from_object(config)

    initialize_extensions(app)
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


def register_cli_commands(app):
    @app.cli.command("init_db")
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo("Initialized the database!")
