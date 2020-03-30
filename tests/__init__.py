from flask import Flask
import pytest
import free_shark
from free_shark.utils import load_config_from_envvar

@pytest.fixture
def app():
    app = free_shark.create_app()
    try:
        app.config.from_pyfile('free_shark.cfg')
        app.config.from_pyfile('db_config.cfg')
    except:
        pass
    app.config['WTF_CSRF_ENABLED'] = False
    d=load_config_from_envvar()
    app.config.from_mapping(d)
    with app.app_context():
        free_shark.db.init_db()
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            free_shark.db.init_db()
        yield client
