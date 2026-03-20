import pytest
from server import app, guestbook_entries


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_entries():
    guestbook_entries.clear()
    yield
    guestbook_entries.clear()
