import pytest

from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code(200)  # Verify whether registration page renders after GET request
    response = client.post(
        'auth/register',
        data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == '/auth/login'

    with app.app_context():  # Verify whether user 'a' exists in the database
        assert get_db().execute(
            "SELECT * FROM user WHERE username == 'a'"
            ).fetchone() is not None


# Using pytest.mark.parametrize to test each possible branch of flaskr.auth.register function
# Thanks to this decorator we do not need to write a for loop in test_reg... function
# We input test response messages as byte strings because response.data contains the body of the response as bytes
@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'already registered')
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
