import pytest

from mabd.app import MABD, Delivery, Offer, Request


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


def test_can_update_delivery_by_id():
    mabd = MABD()
    delivery_id = "recNoBUi8dqEwovSK"

    delivery = mabd.get_record_from_table_by_id("deliveries", delivery_id)

    assert delivery.get_fulfilment() == False
    assert mabd.get_delivery_by_number(3).get_fulfilment() == False

    update_dict = {"fulfilled?": True}

    updated_delivery = mabd.update_delivery(delivery_id, update_dict)

    assert updated_delivery.get_fulfilment() == True
    assert mabd.get_delivery_by_number(3).get_fulfilment() == True


def test_can_get_record_from_table_by_id():
    mabd = MABD()
    record_id0 = "rec1EqOYCFiqjfPFZ"
    request = mabd.get_record_from_table_by_id("requests", record_id0)

    assert type(request) is Request
    assert request.get_id() == record_id0

    record_id1 = "recEwRhLHhsKIdKc4"
    offer = mabd.get_record_from_table_by_id("offers", record_id1)

    assert type(offer) is Offer
    assert offer.get_id() == record_id1

    record_id2 = "recyRmCERIeiniXaJ"
    delivery = mabd.get_record_from_table_by_id("deliveries", record_id2)

    assert type(delivery) is Delivery
    assert delivery.get_id() == record_id2


def test_delivery_get_all_requestIDs_can_handle_deliveries_without_requests():
    mabd = MABD()

    delivery2 = mabd.get_delivery_by_number(2)
    requestIDs = mabd.delivery_get_all_requestIDs(delivery2)

    assert len(requestIDs) == 2

    delivery2_without_requests = mabd.update_delivery(
        delivery2.get_id(), {"requests": []}
    )

    requestIDs = mabd.delivery_get_all_requestIDs(delivery2_without_requests)

    assert requestIDs == []
