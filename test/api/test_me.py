from pytest_schema import schema


def test_me(client, bearer_token):
    HEADERS = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    response = client.get(
            "/me",
            headers=HEADERS,
            )

    assert response.status_code == 200
    assert response.json() == schema({
        "id": str,
        "email": "john.doe@ibm.com",
        "first_name": "john",
        "last_name": "doe"
        })
