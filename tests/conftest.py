import pytest
from app import app, distances


@pytest.fixture(autouse=True)
def reset_distances():
    distances.clear()
    yield
    distances.clear()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c
