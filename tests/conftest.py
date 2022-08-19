import os
import tempfile  # Creating temporary files and file descriptors for testing

import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({  # Creating an instance of app to be used for testing with testing related parameters
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():  # Initializing sqlite db in db_path generated with tempfile.mkstemp and then populating it
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture  # Tests will use the client to run requests, instead of running an actual server
def client(app):
    return app.test_client()


@pytest.fixture  # Similar to the client, but will be used to call the Click (CLI) commands registered with the app
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


# Auth fixture that can be used to login (as the test user, defined in /tests/data.sql) and logout during tests
@pytest.fixture
def auth(client):
    return AuthActions(client)

