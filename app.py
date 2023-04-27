import os
import logging


from flask import make_response
from json import dumps

from routes import blueprint

from modules import create_app
from utils import logger


ENV = os.getenv("FLASK_ENV") or "dev"


app = create_app()
app.register_blueprint(blueprint=blueprint)


app.app_context().push()

DEBUG = app.config.get("DEBUG")
logger.init_logger(level="DEBUG")
logger = logging.getLogger("starter-kit")


@app.route("/ping", methods=["GET"])
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
