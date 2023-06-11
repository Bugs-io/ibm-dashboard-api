from pytest_schema import schema


def test_login(client):
    response = client.post(
            "/login",
            json={
                "email": "john.doe@ibm.com",
                "password": "somepass"
                }
            )

    assert response.status_code == 200
    assert response.json() == schema({
        "id": str,
        "id_token": str,
        "email": "john.doe@ibm.com",
        })


def test_login_raises_error_when_user_not_found(client):
    response = client.post(
            "/login",
            json={
                "email": "jane.doe@ibm.com",
                "password": "somepass"
                }
            )

    assert response.status_code == 404
    assert response.json() == schema({
        "error_code": "USER_DOES_NOT_EXIST"
        })


def test_login_raises_error_when_password_is_invalid(client):
    response = client.post(
            "/login",
            json={
                "email": "john.doe@ibm.com",
                "password": "wrongpass"
                }
            )

    assert response.status_code == 401
    assert response.json() == schema({
        "error_code": "INVALID_PASSWORD"
        })
