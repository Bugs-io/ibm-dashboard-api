from pytest_schema import schema


def test_signup(client):
    response = client.post(
            "/signup",
            json={
                "first_name": "john",
                "last_name": "doe",
                "email": "me@ibm.com",
                "password": "somepass"
                }
            )

    assert response.status_code == 201
    assert response.json() == schema({
        "id": str,
        "id_token": str,
        "email": "me@ibm.com",
        })


def test_signup_raises_error_when_email_is_invalid(client):
    response = client.post(
            "/signup",
            json={
                "first_name": "john",
                "last_name": "doe",
                "email": "me@gmail",
                "password": "somepass"
                }
            )

    assert response.status_code == 400
    assert response.json() == schema({
        "error_code": "INVALID_EMAIL",
        })


def test_signup_raises_error_when_user_already_exists(client):
    response = client.post(
            "/signup",
            json={
                "first_name": "john",
                "last_name": "doe",
                "email": "me@ibm.com",
                "password": "somepass"
                }
            )

    assert response.status_code == 409
    assert response.json() == schema({
        "error_code": "USER_ALREADY_EXISTS",
        })
