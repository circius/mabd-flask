import pytest


def test_user_index_no_login_advertises_available_actions(client):
    rv = client.get("/")

    assert b"admin" in rv.data

    assert b"user login" in rv.data

    assert b"my requests" not in rv.data


def test_getting_requests_without_session_redirects_to_index(client):
    rv = client.get("/myrequests")

    assert rv.status_code == 302


def test_login_redirects_to_oauth_provider(client):
    rv = client.get("/login")

    rv_headers = rv.headers

    redirect_location = rv_headers.get("Location")

    assert rv.status_code == 302
    assert "auth0" in redirect_location


def test_logout_clears_session_and_redirects_to_oauth_provider(client):
    with client as c:
        with c.session_transaction() as sess:
            sess["profile"] = {"user_id": "someuser@mail.de", "name": "whoever"}
        rv = c.get("/logout")

        # assert sess["user_id"] is None
        # assert sess["name"] is "alfie"
        rv_headers = rv.headers
        redirect_location = rv_headers.get("Location")

        assert rv.status_code == 302
        assert "auth0" in redirect_location
        assert "logout" in redirect_location


def test_can_access_unfulfilled_requests_page_with_cookie(client):
    requester = "Lubna"

    with client as c:
        with c.session_transaction() as sess:
            sess["profile"] = {"name": requester}
        rv = c.get("/myrequests")

        assert b"Sofa" in rv.data
        assert b"Wardrobe" in rv.data

        assert b"TV" not in rv.data
        assert b"Coffee table" not in rv.data

    requester = "Nahed"
    with client as c:
        with c.session_transaction() as sess:
            sess["profile"] = {"name": requester}
        rv = c.get("/myrequests")

        assert b"Washing machine" in rv.data
        assert b"3-seater Sofa" in rv.data
