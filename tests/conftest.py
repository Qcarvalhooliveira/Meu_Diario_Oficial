import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/Meu_Diario_Oficial.db'
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
