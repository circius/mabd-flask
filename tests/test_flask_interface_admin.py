# import os

# import pytest


# def test_admin_index(client):
#     admin_email = os.getenv("MABD_FLASK_ADMIN_EMAIL")
#     with client as c:
#         with c.session_transaction() as sess:
#             sess["jwt_payload"] = {"email": admin_email}
#             sess[
#                 "profile"
#             ] = {}  # this is the stupid way I currently handle "logged in or not"

#         rv = client.get("/admin/")
#         print(rv.data)

#         assert b"utilities" in rv.data
#         assert b"delivery fulfilment" in rv.data


# def test_fulfilment_interface_gets_unfulfilled(client, mock_get_airtable):
#     admin_email = os.getenv("MABD_FLASK_ADMIN_EMAIL")
#     with client as c:
#         with c.session_transaction() as sess:
#             sess["jwt_payload"] = {"email": admin_email}
#             sess[
#                 "profile"
#             ] = {}  # this is the stupid way I currently handle "logged in or not"

#     rv = client.get("/admin/fulfilment")

#     assert b"delivery_number" in rv.data

#     assert b"Lubna" in rv.data
#     assert b"Tara" in rv.data

#     assert b"Belen" not in rv.data


# def test_fulfilment_interface_errors_when_asked_to_fulfil_nonexistent_record(client):
#     admin_email = os.getenv("MABD_FLASK_ADMIN_EMAIL")
#     with client as c:
#         with c.session_transaction() as sess:
#             sess["jwt_payload"] = {"email": admin_email}
#             sess[
#                 "profile"
#             ] = {}  # this is the stupid way I currently handle "logged in or not"

#         nosuch_delivery_number = 32
#         rv = client.get(
#             "admin/fulfilment", query_string=dict(delivery_id=nosuch_delivery_number),
#         )

#         error_string = (
#             f"No unfulfilled delivery has the number {nosuch_delivery_number}"
#         )
#         assert bytes(error_string, encoding="utf-8") in rv.data


# ## this test should be reinstated but manual testing for database interaction will
# ## do for now.

# # def test_fulfilment_interface_does_fulfilment(client, mock_get_airtable):
# #     delivery_to_fulfil = 2
# #     rv = client.get("admin/fulfilment", data=dict(delivery_id=delivery_to_fulfil))

# #     assert b"Sam" not in rv.data
# #     assert b"Lubna" not in rv.data
