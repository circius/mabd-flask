import pytest

from mabd.flask_interface import create_app


@pytest.fixture(autouse=True)
def mock_get_all_tables(monkeypatch):
    from testdata import TestData as TD
    from mabd import airtable_interface

    def mock_get_all_tables(table_names):
        return TD()

    monkeypatch.setattr(airtable_interface, "get_all_tables", mock_get_all_tables)
    return True


@pytest.fixture()
def mock_get_airtable(monkeypatch):
    from testdata import TestData as TD
    from mabd import app

    def mock_get_airtable(self, table_name):
        return TD().get_table(table_name)

    monkeypatch.setattr(app.MABD, "get_airtable", mock_get_airtable)
    return True


@pytest.fixture
def app():
    """ create and configure a new flask app instance for each test.
"""
    app = create_app({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
