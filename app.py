import os
import logging

from flask_migrate import Migrate
from flask_cors import CORS
from flask import make_response
from json import dumps

from routes import blueprint
from modules.user import create_app, db
from utils import logger

# for db migrations
# from modules.user.model import User

ENV = os.getenv("FLASK_ENV") or "dev"
DEBUG = os.getenv("DEBUG", True)

app = create_app(ENV)
app.register_blueprint(blueprint=blueprint, url_prefix="/starter-kit")
CORS(app)

app.app_context().push()

migrate = Migrate(app, db)

logger.init_logger(level="DEBUG")
logger = logging.getLogger("starter-kit")


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
