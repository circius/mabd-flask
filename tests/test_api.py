from unittest.mock import patch

from mabd import api, airtable_interface
from mabd.app import MABD

from testdata import TestData as TD


def test_can_get_readable_unfulfilled_deliveries(monkeypatch):
    def mock_get_all_tables(table_names):
        return TD()

    monkeypatch.setattr(airtable_interface, "get_all_tables", mock_get_all_tables)

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
    def mock_get_all_tables(table_names):
        return TD()

    monkeypatch.setattr(airtable_interface, "get_all_tables", mock_get_all_tables)

    deliveries = api.get_pretty_unfulfilled_deliveries()
    assert type(deliveries) is list
    assert "Tara" in deliveries[0]
    assert "Joanna" in deliveries[0]
    assert "Rachael" in deliveries[0]


def test_can_do_delivery_fulfilment(monkeypatch):
    def mock_get_all_tables(table_names):
        return TD()

    monkeypatch.setattr(airtable_interface, "get_all_tables", mock_get_all_tables)

    interface = MABD()
    before_fulfilment = interface.get_delivery_by_number(2)
    print(before_fulfilment)
    assert "fulfilled?" not in before_fulfilment.get_columns()
    fulfilment = interface.do_delivery_fulfilment(2)
    assert "fulfilled?" in fulfilment.get_columns()
    assert fulfilment.get_field("fulfilled?") is True

    # checking that state has been retained
    delivery_2_new_reference = interface.get_delivery_by_number(2)
    assert "fulfilled?" in delivery_2_new_reference.get_columns()
    assert fulfilment.get_field("fulfilled?") is True
