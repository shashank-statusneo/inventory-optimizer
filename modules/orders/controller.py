import logging

from flask import request
from flask_restx import Resource

from modules.orders.schema import OrderSchema
from utils.requests import auth_required
from modules.orders.service import create_new_order

order_api = OrderSchema.api
order_schema = OrderSchema.schema


logger = logging.getLogger("starter-kit")


@order_api.route("/")
class Order(Resource):
    """
    Args:
        Resource (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        logger.info("in order main class init")
        super().__init__(*args, **kwargs)

    @auth_required
    @order_api.expect(order_schema, validate=True)
    def post(self):
        """_summary_"""

        logger.info("in User module post")

        request_data = request.json
        return create_new_order(request_data)
