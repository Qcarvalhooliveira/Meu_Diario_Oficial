import pytest
from app import create_app, db
import os

@pytest.fixture(scope='module')
def test_client():
    os.environ['DATABASE_URL'] = 'postgresql://test_user:test_password@localhost:5433/test_db'
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    yield db  # Este yield retorna o banco de dados para uso nos testes

    db.drop_all()
