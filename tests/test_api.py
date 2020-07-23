from mabd import api, airtable_interface
from mabd.app import MABD, Delivery


def test_can_get_readable_unfulfilled_deliveries(monkeypatch, mock_get_airtable):
    deliveries = api.get_readable_unfulfilled_deliveries()
    assert len(deliveries) == 2

    delivery_3 = [
        delivery for delivery in deliveries if delivery["delivery_number"] == 3
    ][0]

    assert delivery_3["date"] == "2020-05-24"
    assert delivery_3["driver"] == "Rachael"
    assert delivery_3["from"] == "Joanna"
    assert delivery_3["to"] == "Tara"

    delivery_1 = [
        delivery for delivery in deliveries if delivery["delivery_number"] == 1
    ]

    assert delivery_1 == []


def test_can_get_pretty_unfulfilled_deliveries(monkeypatch, mock_get_airtable):
    deliveries = api.get_pretty_unfulfilled_deliveries()

    assert type(deliveries) is list
    assert "Tara" in deliveries[0]
    assert "Joanna" in deliveries[0]
    assert "Rachael" in deliveries[0]

    for delivery in deliveries:
        assert "Belen" not in delivery


def test_can_do_delivery_fulfilment(monkeypatch, mock_get_airtable):
    interface = MABD()

    before_fulfilment = interface.get_delivery_by_number(2)
    before_fulfilment_columns = before_fulfilment.get_columns()
    assert "fulfilled?" not in before_fulfilment_columns

    fulfilment = api.do_delivery_fulfilment(2)
    assert type(fulfilment) is Delivery
    fulfilment_columns = fulfilment.get_columns()
    assert "fulfilled?" in fulfilment_columns
    assert fulfilment.get_field("fulfilled?") is True


def test_can_get_readable_unfulfilled_requests_for_extant_person(mock_get_airtable):
    requester = "Lubna"
    request_reps = api.get_readable_unfulfilled_requests_of_person(requester)

    assert type(request_reps) == list
    assert len(request_reps) == 2
    assert type(request_reps[0]) == dict

    items = [request_rep["item"] for request_rep in request_reps]
    assert "Sofa" in items
    assert "Wardrobe" in items

    assert "TV" not in items
    assert "Coffee table" not in items

    requester = "Nahed"
    request_reps = api.get_readable_unfulfilled_requests_of_person(requester)

    items = [request_rep["item"] for request_rep in request_reps]
    assert "Washing machine" in items
    assert "3-seater Sofa" in items

    requester = "no-one"
    request_reps = api.get_readable_unfulfilled_requests_of_person(requester)

    assert type(request_reps) == list
    assert len(request_reps) == 0


def test_can_get_readable_matching_offers_for_requestID():
    requestID = "rect8dK5CN0kF4f5F"
    matching_offer_dicts = api.get_readable_matching_offers_for_requestID(requestID)

    offer_names = [
        matching_offer_dict["item_name"] for matching_offer_dict in matching_offer_dicts
    ]
    assert "Four-seater Ikea sofa + footstool" in offer_names


def test_can_get_readable_offer_by_offer_uid():
    offer_number = 1
    offer = api.get_readable_offer_by_offer_number(offer_number)

    assert offer["donor"] == "katie"
    assert "kitchen bits" in offer["item_name"]
