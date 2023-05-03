# """
# This file (test_orders.py) contains the functional tests for the `users`.
# These tests use GETs and POSTs to different URLs to check
# for the proper behavior of the `users` blueprint.
# """
# from modules.orders.model import Orders
# from modules.users.model import Users
# from modules import db
# from json import loads


# def test_new_order(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/order' route is requested (POST)
#     THEN check the response is valid

#     """

#     response = test_client.post(
#         path="/user/",
#         json={
#             "email": "test_user@gmail.com",
#             "username": "test_user",
#             "password": "test_password",
#         },
#     )
#     assert response.status_code == 201

#     res = loads(response.data)
#     res_data = res.get("data")
#     auth_token = res_data.get("auth_token")

#     # check validity of auth_token
#     assert isinstance(auth_token, str)

#     response = test_client.post(
#         path="/order/",
#         json={
#             "amount": 100.00,
#             "user_id": 1,
#         },
#         headers={"Authorization": auth_token},
#     )
#     assert response.status_code == 201

#     res = loads(response.data)
#     res_data = res.get("data")
#     order_id = res_data.get("id")

#     assert order_id

#     # delete user
#     Users.query.filter_by(email="test_user@gmail.com").delete()
#     # delete order
#     Orders.query.filter_by(id=order_id).delete()
#     db.session.commit()
