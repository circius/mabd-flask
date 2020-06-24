from mabd import airtable_interface


def test_can_get_list_of_unfulfilled_deliveries(monkeypatch):
    monkeypatch.setenv("BASE_ID", "appGDD6qBhKjufAIO")


def test_can_get_tables():
    some_table_names = ["deliveries", "requests", "drivers"]
    some_tables = airtable_interface.get_all_tables(some_table_names)
    assert type(some_tables) is dict
    for name in some_tables:
        assert name in some_tables.keys()
    record = some_tables["deliveries"].get_all()[0]
    fields = record["fields"]
    for key in ["date", "driver", "dropoff_time"]:
        assert key in fields.keys()


    
