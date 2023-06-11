import os
import pytest
import tempfile
from fastapi.testclient import TestClient

from app.interface.api import app
from app.infrastructure.ponyorm.database import db


TEST_USER = {
        "first_name": "john",
        "last_name": "doe",
        "email": "john.doe@ibm.com",
        "password": "somepass"
        }


@pytest.fixture(scope='session')
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def setup_test_db(client):
    temp_file = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False)
    temp_file.close()

    db.bind(provider='sqlite', filename=temp_file.name, create_db=True)
    db.generate_mapping(create_tables=True)

    seed_test_database(client)

    yield db

    db.disconnect()
    db.drop_all_tables(with_all_data=True)

    os.remove(temp_file.name)


def seed_test_database(client):
    client.post("/signup", json=TEST_USER)


@pytest.fixture(scope='session')
def bearer_token(client):
    response = client.post("/login", json=TEST_USER)

    token = response.json()["id_token"]

    return token
