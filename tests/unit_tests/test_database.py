import pytest
from database import Database, NULL


def test_set():
    db = Database()
    db.set('key', 'value')
    assert db.get('key') == 'value'


def test_get():
    db = Database()
    assert db.get('key') == NULL
    db.set('key', 'value')
    assert db.get('key') == 'value'


def test_unset():
    db = Database()
    db.set('key', 'value')
    assert db.unset('key') is None
    assert db.get('key') == NULL


def test_counts():
    db = Database()
    db.set('key1', 'value')
    db.set('key2', 'value')
    assert db.counts('value') == 2
    assert db.counts('other_value') == 0


def test_find():
    db = Database()
    db.set('key1', 'value')
    db.set('key2', 'value')
    db.set('key3', 'other_value')
    assert db.find('value') == ['key1', 'key2']
    assert db.find('other_value') == ['key3']


def test_begin_rollback_commit():
    db = Database()
    db.begin()
    db.set('key', 'value')
    db.rollback()
    assert db.get('key') == NULL
    db.begin()
    db.set('key', 'value')
    db.commit()
    assert db.get('key') == 'value'


def test_rollback_without_begin():
    db = Database()
    with pytest.raises(IndexError):
        db.rollback()


def test_commit_without_begin():
    db = Database()
    with pytest.raises(IndexError):
        db.commit()
