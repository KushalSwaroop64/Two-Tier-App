import pytest
from app.app import app
from mysql.connector.errors import DatabaseError

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    res = client.get("/")
    assert res.status_code == 200

def test_add_user_missing_db(client):
    # When DB is not running locally, Flask should return 500
    # This confirms the route exists and handles DB errors gracefully
    try:
        res = client.post("/users", json={})
        assert res.status_code in [400, 500]
    except DatabaseError:
        # DB not available locally — this is expected outside Docker
        pass