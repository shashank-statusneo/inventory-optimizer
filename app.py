import os
import logging


from flask import make_response
from json import dumps


from modules import create_app
from utils import logger
from routes import blueprint


ENV = os.getenv("FLASK_ENV") or "dev"
# Get Flask App
app = create_app(ENV)

# Register module blueprints
app.register_blueprint(blueprint=blueprint)


logger.init_logger(level="DEBUG")
logger = logging.getLogger("starter-kit")


@app.route("/ping", methods=["GET"])
def ping():
    response = {
        "success": True,
        "env": {
            "RUN_FLASK_ENV": os.getenv("FLASK_ENV") or "dev",
        },
    }
    response = make_response(dumps(response), 200)
    response.headers["content-type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
