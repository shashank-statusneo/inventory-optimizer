from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource

from main.modules.inventory_optimizer.schema_validator import AddDemandForecastSchema
from main.utils import get_data_from_request_or_raise_validation_error


demand_forecast_api = AddDemandForecastSchema.api
# demand_forecast_schema = AddDemandForecastSchema.schema

@demand_forecast_api.route("/")
class DemandForecastApi(Resource):

    def post(self):
        """
        This function is used to add new demand forecast.
        :return:
        """
        # data = get_data_from_request_or_raise_validation_error(demand_forecast_schema, request.files)
        data = request.files
        print (data)
        # data.update({"user_id": auth_user.id})
        # address_id = AddressController.add_address(data)
        # response = make_response(
        #     jsonify({"message": "Address added", "location": f"/addresses/{address_id}", "id": address_id}), 201
        # )
        # response.headers["Location"] = f"/addresses/{address_id}"
        return True, 200


# class AddressApi2(CacheResource):
#     method_decorators = [jwt_required()]

#     def get(self, address_id: int):
#         """
#         This function is used to get the particular address by address_id
#         :param address_id:
#         :return:
#         """
#         auth_user = AuthUserController.get_current_auth_user()
#         response = AddressController.get_address_by_address_id(address_id, auth_user)
#         return jsonify(response)

#     def put(self, address_id: int):
#         """
#         This function is used to update the address by address_id
#         :param address_id:
#         :return:
#         """
#         auth_user = AuthUserController.get_current_auth_user()
#         data = get_data_from_request_or_raise_validation_error(UpdateAddressSchema, request.json)
#         response = AddressController.update_address(address_id, data, auth_user)
#         return jsonify(response)

#     def delete(self, address_id: int):
#         """
#         This function is used to delete the address by address_id.
#         :param address_id:
#         :return:
#         """
#         auth_user = AuthUserController.get_current_auth_user()
#         response = AddressController.delete_address(address_id, auth_user)
#         return jsonify(response)


# inventory_optimizer_namespace = Namespace("inventory_optimizer", description="Inventory Optimizer Operations")
# inventory_optimizer_namespace.add_resource(DemandForecastApi, "/demand_forecast")
