from mabd import api, airtable_interface
from mabd.app import MABD


def test_can_get_readable_unfulfilled_deliveries(monkeypatch):
    deliveries = api.get_readable_unfulfilled_deliveries()
    assert len(deliveries) == 3
    delivery_1 = [
        delivery for delivery in deliveries if delivery["delivery_number"] == 1
    ][0]
    assert delivery_1["date"] == "2020-05-24"
    assert delivery_1["driver"] == "Weez"
    assert delivery_1["from"] == "Hartingdon"
    assert delivery_1["to"] == "Belen"


def test_can_get_pretty_unfulfilled_deliveries(monkeypatch):
    deliveries = api.get_pretty_unfulfilled_deliveries()
    assert type(deliveries) is list
    assert "Tara" in deliveries[0]
    assert "Joanna" in deliveries[0]
    assert "Rachael" in deliveries[0]


def test_can_do_delivery_fulfilment(monkeypatch):
    interface = MABD()

    before_fulfilment = interface.get_delivery_by_number(2)
    before_fulfilment_columns = before_fulfilment.get_columns()
    assert "fulfilled?" not in before_fulfilment_columns

    fulfilment = api.do_delivery_fulfilment(2)
    fulfilment_columns = fulfilment.get_columns()
    assert "fulfilled?" in fulfilment_columns
    assert fulfilment.get_field("fulfilled?") is True
