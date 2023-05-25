# Business logic for inventory_optimizer

import logging

from utils.exceptions import (
    DatabaseErrorException,
)
from datetime import datetime

from modules import db
from modules.inventory_optimizer.model import MasterData, DemandForecast, Vendor
from utils.misc import csv_to_dict

logger = logging.getLogger("starter-kit")


def create_new_demand_forecast(data):
    """
    Creates a new user

    Args:
        data (dict):
            email (str): user email
            username(str): user name
            password (str): user password

    Returns:
        id (int): new user id
        public_id (str): new user public id
    """

    logger.info("in create_new_demand_forecast")

    response = {"success": True, "data": []}

    # return response, 200

    raw_file = data.get("file")

    file_data = csv_to_dict(csv_file=raw_file)

    file_data = file_data[0]

    new_demand_forecast = DemandForecast(
        weekend=datetime.strptime(file_data.get("weekend"), "%d/%m/%y"),
        month_no=file_data.get("month_no"),
        month_week=file_data.get("month_week"),
        article=file_data.get("article"),
        site=file_data.get("site"),
    )

    save_changes(new_demand_forecast)

    master_id = create_new_master_data(
        file_id=new_demand_forecast.id,
        file_name=raw_file.filename,
        file_type="demand_forecast",
        file_ext=raw_file.mimetype,
        file_object=raw_file,
    )

    response["data"] = {"id": new_demand_forecast.id, "master_id": master_id}
    response["message"] = "Demand Forecast Created Successfully"

    return response, 201


def create_new_vendor(data):
    """
    Creates a new user

    Args:
        data (dict):
            email (str): user email
            username(str): user name
            password (str): user password

    Returns:
        id (int): new user id
        public_id (str): new user public id
    """

    logger.info("in create_new_vendor")

    response = {"success": True, "data": []}

    raw_file = data.get("file")

    file_data = csv_to_dict(csv_file=raw_file)

    file_data = file_data[0]

    new_vendor = Vendor(
        vendor_id=file_data.get("vendor_id"),
        lead_time_avg=file_data.get("lead_time_avg"),
        lead_time_std_dev=file_data.get("lead_time_std_dev"),
        price=file_data.get("price"),
        order_cost=file_data.get("order_cost"),
        stockout_cost=file_data.get("stockout_cost"),
    )

    save_changes(new_vendor)

    master_id = create_new_master_data(
        file_id=new_vendor.id,
        file_name=raw_file.filename,
        file_type="demand_forecast",
        file_ext=raw_file.mimetype,
        file_object=raw_file,
    )

    response["data"] = {"id": new_vendor.id, "master_id": master_id}
    response["message"] = "Vendor Created Successfully"

    return response, 201


def create_new_master_data(
    file_id: int, file_name: str, file_type: str, file_ext: str, file_object: bytes
):
    """
    Creates a new master data

    args:
        file_id (int): file id of the file record
        file_name (str): file name
        file_type (str): file type eg - demand_forecast, vendor
        file_ext (str): file extenstion eg - csv, xls
        file_object (bytes): file object

    returns:
        id (int): id for created master data entry
    """

    new_master_data = MasterData(
        file_id=file_id,
        file_name=file_name,
        file_type=file_type,
        file_ext=file_ext,
        file_object=file_object,
    )

    save_changes(new_master_data)

    return new_master_data.id


def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        raise DatabaseErrorException(
            debug_message=f"{e}", error_message="Databse Error Occured"
        )
