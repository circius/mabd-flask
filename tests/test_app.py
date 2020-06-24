from mabd import app, airtable_interface

import testdata

# def test_can_get_all_data():
#     airtable_dicts = app.table_names_get_all_data(app.TABLE_NAMES)
#     assert type(airtable_dicts) is dict
#     for key in airtable_dicts.keys():
#         assert key in app.TABLE_NAMES
#         assert type(airtable_dicts[key]) is list


def test_can_get_all_requestIDs_fulfilled_by_delivery():
    deliveries = testdata.test_matching["deliveries"]
    first_delivery = [el for el in deliveries if el["fields"]["id"] == 1][0]
    returned_requests = app.delivery_get_all_requestIDs(first_delivery)
    assert len(returned_requests) == 3


def test_can_get_confirmed_offer_from_request():
    requestID = "rec4hBg7aLIxYl3RO"
    request = table_get_request(requestID)
    assert (
        app.request_get_confirmed_offerID(request)
        == request["fields"]["confirmed_offer"][0]
    )


def test_can_get_matching_offers_from_request():
    requestID = "recD0pKjK9LMIm7k7"
    request = table_get_request(requestID)
    assert (
        app.request_get_matching_offerIDs(request)
        == request["fields"]["matching_offers"]
    )


def table_get_request(id: str):
    """consumes an airtable id and returns the request with that id from
the testdata, or None.

    """
    requests = testdata.test_matching["requests"]

    def predicate(el):
        return el["id"] == id

    request_or_None = [el for el in requests if predicate(el)]
    return None if request_or_None is None else request_or_None[0]
