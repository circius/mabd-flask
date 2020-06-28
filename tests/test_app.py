from unittest.mock import patch

from mabd.app import MABD

from testdata import TestData as TD


def test_can_get_all_requestIDs_fulfilled_by_delivery():
    deliveries = TD().get_table("deliveries")
    first_delivery = deliveries.match("id", 1)
    returned_requests = MABD().delivery_get_all_requestIDs(first_delivery)
    assert len(returned_requests) == 3


def test_can_get_confirmed_offer_from_request():
    requests = TD().get_table("requests")
    requestID = "rec4hBg7aLIxYl3RO"
    request = requests.get(requestID)
    assert (
        MABD().request_get_confirmed_offerID(request)
        == request.get_field("confirmed_offer")[0]
    )


def test_can_get_matching_offers_from_request():
    requests = TD().get_table("requests")
    requestID = "recD0pKjK9LMIm7k7"
    request = requests.get(requestID)
    assert MABD().request_get_matching_offerIDs(request) == request.get_record_field(
        "matching_offers"
    )
