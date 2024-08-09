from app import db, create_app
from app.models import User, Subscription
import pytest

@pytest.fixture(scope='module')
def new_user():
    user = User(name='Test User', email='test@example.com')
    user.set_password('my_secure_password')  # Definindo a senha
    return user

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_new_user(new_user):
    assert new_user.name == 'Test User'
    assert new_user.email == 'test@example.com'
    assert new_user.password_hash is not None  # Verifica se a senha foi hashada

def test_check_password(new_user):
    assert new_user.check_password('my_secure_password') == True  # Senha correta
    assert new_user.check_password('wrong_password') == False     # Senha incorreta

