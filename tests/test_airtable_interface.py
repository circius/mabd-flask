from mabd import airtable_interface


def test_can_get_list_of_unfulfilled_deliveries(monkeypatch):
    monkeypatch.setenv("BASE_ID", "appGDD6qBhKjufAIO")


def test_can_get_tables_from_test_base(monkeypatch):
    monkeypatch.setenv("BASE_ID", "appGDD6qBhKjufAIO")
    all_tables = airtable_interface.get_all_tables(airtable_interface.TABLE_NAMES)
    assert type(all_tables) is dict
    for name in airtable_interface.TABLE_NAMES:
        assert name in all_tables.keys()
