import os
import logging

import traceback

from flask_migrate import Migrate
from flask_cors import CORS
from flask import make_response
from json import dumps
from werkzeug.exceptions import HTTPException

from routes import blueprint
from modules import create_app, db
from utils import logger
from utils.exceptions import APIException

from config import config_by_name

ENV = os.getenv("FLASK_ENV") or "dev"
config = config_by_name[ENV]


app = create_app(config)
app.register_blueprint(blueprint=blueprint, url_prefix="/starter-kit")
CORS(app)


app.app_context().push()

DEBUG = app.config.get("DEBUG")

migrate = Migrate(app, db)

logger.init_logger(level="DEBUG")
logger = logging.getLogger("starter-kit")

app.config["PROPAGATE_EXCEPTIONS"] = True


@app.after_request
def after_request_func(response):
    """
    runs after the request is completed
    add after request modifications here
    to the response object
    """

    logger.info("after request is running")
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(err):
    """Return JSON instead of HTML for HTTP errors."""
    logger.info("HTTPException errorhandler is running!")
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
