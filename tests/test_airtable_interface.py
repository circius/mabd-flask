from mabd import airtable_interface


def test_can_get_tables():
    some_table_names = ["deliveries", "requests", "drivers"]
    some_tables = airtable_interface.get_all_tables(some_table_names)
    for name in some_table_names:
        assert name in some_tables.keys()
    record = some_tables["deliveries"].get_all()[0]
    fields = record["fields"]
    for key in ["date", "driver", "dropoff_time"]:
        assert key in fields.keys()
