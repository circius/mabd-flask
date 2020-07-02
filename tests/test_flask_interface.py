import pytest


def test_admin_index(client):
    index = client.get("/")
    assert index is None
