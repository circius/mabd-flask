"""this code is derived from the testing suite for the
airtable-python-wrapper library, adapted to test this partcular
application.

"""
import pytest


@pytest.fixture(autouse=True)
def mock_get_all_tables(monkeypatch):
    from testdata import TestData as TD
    from mabd import airtable_interface

    def mock_get_all_tables(table_names):
        return TD()

    monkeypatch.setattr(airtable_interface, "get_all_tables", mock_get_all_tables)
