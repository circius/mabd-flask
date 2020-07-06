import pytest


def test_user_index_advertises_available_tools(client):
    rv = client.get("/")

    assert b"admin login" in rv.data

    assert b"my requests" in rv.data


def test_getting_requests_requires_cookie(client):
    rv = client.get("/myrequests")

    assert rv.status_code == 403


def test_can_access_requests_page_with_cookie(client):
    client.set_cookie("localhost", "user", "Tara")
    rv = client.get("/myrequests")

    assert b"Tara's requests" in rv.data
