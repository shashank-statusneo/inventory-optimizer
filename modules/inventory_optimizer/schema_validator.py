#  Store api data transfer models

from flask_restx import Namespace, fields


class AddDemandForecastSchema:
    """
    Schema to add demand forecast to the database.
    """
    api = Namespace("demand_forecast",
                    description="Demand Forecast Operations")
    # schema = api.model(fields.Raw(type="file"))

    # weekend = fields.String(required=True)
    # month_no = fields.Integer(required=True)
    # month_week = fields.Integer(required=True)
    # article = fields.String(required=True)
    # site = fields.String(required=True)


class AddVendorSchema:
    """
    Schema to add vendor to the database.
    """

    api = Namespace("vendor",
                    description="Vendor Operations")

    # vendor_data = fields.Raw(type="file")
    # lead_time_avg = fields.Float(required=True)
    # price = fields.Float(required=True)
    # order_cost = fields.Float(required=True)
    # stockout_cost = fields.Float(required=True)
