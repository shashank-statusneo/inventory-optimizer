#  Store api data transfer models


from flask_restx import Namespace, fields


class OrderSchema:
    api = Namespace("order", description="Order operations")
    schema = api.model(
        "order",
        {
            "user_id": fields.Integer(required=True, description="user id"),
            "amount": fields.Float(required=True, description="order amount"),
        },
    )
