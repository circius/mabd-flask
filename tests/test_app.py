import pytest

from mabd.app import MABD, Delivery, Offer, Request, Record


def test_can_get_all_requestIDs_fulfilled_by_delivery():
    mabd = MABD()
    deliveries = mabd.get_airtable("deliveries")
    first_delivery = mabd.get_delivery_by_number(1)
    returned_requests = first_delivery.get_all_requestIDs()
    assert len(returned_requests) == 3


def test_MABD_do_delivery_fulfilment_returns_false_if_delivery_does_not_exist():
    mabd = MABD()
    result = mabd.do_delivery_fulfilment(3002)
    assert result == False


def test_can_get_confirmed_offer_from_request():
    mabd = MABD()
    request = mabd.get_record_from_table_by_id("requests", "rec4hBg7aLIxYl3RO")
    assert request.get_confirmed_offerID() == "reche1z3Dtfexpa8n"

    request2 = mabd.get_record_from_table_by_id("requests", "rec1EqOYCFiqjfPFZ")
    assert request.get_confirmed_offerID() == None


def test_can_get_matching_offers_from_request():
    mabd = MABD()
    request = mabd.get_record_from_table_by_id("requests", "recHE4q1ZkuXpUcde")
    assert request.get_matching_offerIDs() == ["recbuFMiAi5wNCswt"]


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
    requestIDs = delivery2.get_all_requestIDs()

    assert len(requestIDs) == 2

    delivery2_without_requests = mabd.update_delivery(
        delivery2.get_id(), {"requests": []}
    )

    requestIDs = delivery2_without_requests.get_all_requestIDs()

    assert requestIDs == []


def test_Record_can_imitate_record_dict():
    mabd = MABD()
    record = mabd.get_record_from_table_by_id("people", "rec1BI0ZJlxZ0xUnI")

    assert record["id"] == "rec1BI0ZJlxZ0xUnI"
    assert record["fields"]["name"] == "Caroline"
    assert record["createdTime"] == "2020-05-23T17:06:03.000Z"


def test_get_generic_record_for_records_without_subclassed_datastructures():
    mabd = MABD()

    person1 = mabd.get_record_from_table_by_id("people", "rec1BI0ZJlxZ0xUnI")
    assert type(person1) is Record

    driver1 = mabd.get_record_from_table_by_id("drivers", "rec0UsfN8i2IYAtZC")
    assert type(driver1) is Record

    status1 = mabd.get_record_from_table_by_id("statuses", "rec370ei78Jt6y7w6")
    assert type(status1) is Record


def test_Delivery_prints_itself_nicely(capsys):
    mabd = MABD()
    delivery = mabd.get_delivery_by_number(1)

    print(delivery)
    captured = capsys.readouterr()

    assert "Delivery with" in captured.out
    assert "fulfilled?: True" in captured.out
    assert "number: 1" in captured.out


def test_getting_non_existent_record_from_table_returns_None():
    mabd = MABD()

    no_record = mabd.get_record_from_table_by_id("requests", "blahhhh")
    assert no_record is None


def test_can_get_unfulfilled_requests_for_person():
    mabd = MABD()
    requester = "Lubna"
    requests = mabd.get_unfulfilled_requests_of_person(requester)

    request_items = [request.get_field("item") for request in requests]

    assert "Sofa" in request_items
    assert "Wardrobe" in request_items

    assert "TV" not in request_items
    assert "Coffee table" not in request_items


def test_can_get_person_record_by_name():
    mabd = MABD()
    person_name = "Lubna"
    person_record = mabd.get_person_by_person_name(person_name)

    assert person_record is not False
    assert type(person_record) is Record

    assert person_record.get_id() == "rec95fxPGFAmWsi0I"

    person_name = "No-one"
    person_record = mabd.get_person_by_person_name(person_name)

    assert person_record is False


def test_can_get_minimal_representation_from_record():
    mabd = MABD()

    record = mabd.get_record_from_table_by_id("requests", "rec1EqOYCFiqjfPFZ")

    minimal_representation = mabd.request_get_minimal_representation(record)

    for key in ["item", "requested_by"]:
        assert key in minimal_representation.keys()

    assert minimal_representation["item"] == "Chest of drawers"
    assert minimal_representation["requested_by"] == "Ayoub"


def test_can_get_readable_representation_of_matching_offers_by_requestID():
    mabd = MABD()
    requestID = "rect8dK5CN0kF4f5F"
    offer_dicts = mabd.get_readable_matching_offers_for_requestID(requestID)

    assert type(offer_dicts) is list
    assert len(offer_dicts) == 1
    assert offer_dicts[0]["item_name"] == "Four-seater Ikea sofa + footstool"
