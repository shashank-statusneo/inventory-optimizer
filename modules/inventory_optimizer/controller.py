import logging

from flask import request
from flask_restx import Resource
from modules.inventory_optimizer.schema_validator import (
    AddDemandForecastSchema,
    AddVendorSchema,
)
from modules.inventory_optimizer.service import (
    create_new_demand_forecast,
    create_new_vendor,
)

demand_forecast_api = AddDemandForecastSchema.api
vendor_api = AddVendorSchema.api

logger = logging.getLogger("starter-kit")


@demand_forecast_api.route("/")
class DemandForecast(Resource):
    """
    Args:
        Resource (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        logger.info("in Demand Forecast main class init")
        super().__init__(*args, **kwargs)

    def post(self):
        """_summary_"""

        logger.info("in Demand Forecast module post")

        request_data = request.files
        return create_new_demand_forecast(request_data)


@vendor_api.route("/")
class Vendor(Resource):
    """
    Args:
        Resource (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        logger.info("in Vendor main class init")
        super().__init__(*args, **kwargs)

    def post(self):
        """_summary_"""

        logger.info("in Vendor module post")

        request_data = request.files
        print(request.headers)
        return create_new_vendor(request_data)
