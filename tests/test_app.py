from mabd.app import MABD


def test_can_get_all_requestIDs_fulfilled_by_delivery():
    mabd = MABD()
    deliveries = mabd.get_airtable("deliveries")
    first_delivery = deliveries.match("id", 1)
    returned_requests = mabd.delivery_get_all_requestIDs(first_delivery)
    assert len(returned_requests) == 3


def test_can_get_confirmed_offer_from_request():
    mabd = MABD()
    requests = mabd.get_airtable("requests")
    requestID = "rec4hBg7aLIxYl3RO"
    request = requests.get(requestID)
    assert (
        mabd.request_get_confirmed_offerID(request)
        == request.get_field("confirmed_offer")[0]
    )


def test_can_get_matching_offers_from_request():
    mabd = MABD()
    requests = mabd.get_airtable("requests")
    requestID = "recD0pKjK9LMIm7k7"
    request = requests.get(requestID)
    assert mabd.request_get_matching_offerIDs(request) == request.get_record_field(
        "matching_offers"
    )
