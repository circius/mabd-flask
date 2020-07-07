import pytest


def test_user_index_no_login_advertises_available_actions(client):
    rv = client.get("/")

    assert b"admin" in rv.data

    assert b"user login" in rv.data


def test_getting_requests_requires_cookie(client):
    rv = client.get("/myrequests")

    assert rv.status_code == 403


def test_can_login(client):
    rv = client.get("/login/Lubna", follow_redirects=True)

    assert b"welcome, Lubna" in rv.data
    assert b"logout" in rv.data
    assert b"login" not in rv.data


def test_visiting_the_login_page_when_not_logged_in_shows_information_about_logging_in(
    client,
):
    rv = client.get("/login")

    assert b"You are not logged in." in rv.data
    assert b"To login, click the login-link in the email you received." in rv.data
    assert b"If you have lost the email, click here to request a new one." in rv.data


def test_can_access_unfulfilled_requests_page_with_cookie(client):
    requester = "Lubna"
    client.set_cookie("localhost", "user", requester)
    rv = client.get("/myrequests")

    print(rv.data)
    assert b"Lubna&#39;s requests" in rv.data

    assert b"Sofa" in rv.data
    assert b"Wardrobe" in rv.data

    assert b"TV" not in rv.data
    assert b"Coffee table" not in rv.data

    requester = "Nahed"
    client.set_cookie("localhost", "user", requester)
    rv = client.get("/myrequests")

    assert b"Nahed&#39;s requests" in rv.data

    assert b"Washing machine" in rv.data
    assert b"3-seater Sofa" in rv.data


def test_can_get_list_of_matching_offers_for_requests(client):
    requester = "Lubna"
    client.set_cookie("localhost", "user", requester)
    rv = client.get("/myrequests/rect8dK5CN0kF4f5F")

    assert b"matching offers for Sofa" in rv.data

    assert b"Four-seater Ikea sofa" in rv.data
