from sqlalchemy import BLOB
import datetime
from modules import db


class MasterData(db.Model):
    """
    Model for master data.
    """

    __tablename__ = "master_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_ext = db.Column(db.String(50))
    file_object = db.Column(BLOB)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(
        self,
        file_id: int,
        file_name: str,
        file_type: str,
        file_ext: str,
        file_object: bytes,
    ):
        """Create a new master data object
        """
        self.file_id = file_id
        self.file_name = file_name
        self.file_type = file_type
        self.file_ext = file_ext
        self.file_object = file_object
        self.created_at = datetime.datetime.utcnow()


class DemandForecast(db.Model):
    """
    Model for demand forecast data.
    """

    __tablename__ = "demand_forecast"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weekend = db.Column(db.DateTime, nullable=False)
    month_no = db.Column(db.Integer, nullable=False)
    month_week = db.Column(db.Integer, nullable=False)
    article = db.Column(db.String(50), nullable=False)
    site = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(
        self,
        weekend: str,
        month_no: int,
        month_week: int,
        article: str,
        site: str,
    ):
        """Create a new demand forecast data object
        """
        self.weekend = weekend
        self.month_no = month_no
        self.month_week = month_week
        self.article = article
        self.site = site
        self.created_at = datetime.datetime.utcnow()


class Vendor(db.Model):
    """
    Model for vendor data.
    """

    __tablename__ = "vendor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.String(50), nullable=False)
    lead_time_avg = db.Column(db.Float, nullable=False)
    lead_time_std_dev = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_cost = db.Column(db.Float, nullable=False)
    stockout_cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime)

    def __init__(
        self,
        vendor_id: str,
        lead_time_avg: float,
        lead_time_std_dev: float,
        price: float,
        order_cost: float,
        stockout_cost: float
    ):
        """Create a new vendor data object
        """
        self.vendor_id = vendor_id
        self.lead_time_avg = lead_time_avg
        self.lead_time_std_dev = lead_time_std_dev
        self.price = price
        self.order_cost = order_cost
        self.stockout_cost = stockout_cost
        self.created_at = datetime.datetime.utcnow()
