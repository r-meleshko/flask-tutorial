import sqlite3

import pytest

from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():  # Test whether get_db returns the same connection every time
        db = get_db()
        assert db == get_db()

    # Assert that the code below raises expected exception. Should be clause because app.teardown_appcontext(close_db)
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder:  # Create a Recorder class that will be used to record actions performed by test functions
        called = False

    def fake_init_db():
        Recorder.called = True

    # When running test, replace (monkeypatch) init_db function in flaskr.db module by fake_init_db function
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    # Run Click init-db function that initializes db (replaced by fake_init_db) and returns str 'Initialized ...'
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output  # Check whether click.echo executed correctly
    assert Recorder.called  # Check whether fake_init_db function was called
