import os
import logging
import traceback

from flask_migrate import Migrate
from flask_cors import CORS
from flask import make_response
from json import dumps

from routes import blueprint
from modules.user import create_app, db
from utils import logger
from helpers.exceptions import APIException

# for db migrations
# from modules.user.model import User
# from modules.user.blacklist_model import BlacklistToken

ENV = os.getenv("FLASK_ENV") or "dev"
DEBUG = os.getenv("DEBUG", True)

app = create_app(ENV)
app.register_blueprint(blueprint=blueprint, url_prefix="/starter-kit")
CORS(app)

app.app_context().push()

migrate = Migrate(app, db)

logger.init_logger(level="DEBUG")
logger = logging.getLogger("starter-kit")


@app.errorhandler(APIException)
def handle_custom_exception(error):
    """Return a custom message and 400 status code"""

    logger.info("APIException errorhandler is running!")

    response = {
        "success": False,
        "data": [],
        "error_code": error.starter_kit_code,
        "error_message": error.message,
        "debug_message": error.debug_message,
    }

    return response, error.http_code


@app.errorhandler(Exception)
def internal_error(error):
    """runs if any code level error has occured"""

    logger.info("Exception errorhandler is running!")
    # send proper error message rather than html broken response
    trace_err = traceback.format_exc()
    logger.warning(trace_err)

    response = {
        "success": False,
        "data": [],
        "error": "Internal Server Error",
        "debug_message": str(error),
        "traceback": trace_err,
    }
    return response, 500


@app.route("/starter-kit/ping", methods=["GET"])
def ping():
    response = {
        "success": True,
        "env": {
            "RUN_FLASK_ENV": ENV,
        },
    }
    response = make_response(dumps(response), 200)
    response.headers["content-type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0")
