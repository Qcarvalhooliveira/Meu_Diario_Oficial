from app import db, create_app
from app.models import User
import pytest

@pytest.fixture(scope='function')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_new_user(test_client):
    user = User(name='Test User', email='test@example.com')
    user.set_password('my_secure_password')
    db.session.add(user)
    db.session.commit()
    
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'
    assert user.password_hash is not None  # Verifica se a senha foi hashada
    assert user.id is not None  # Verifica se o ID foi gerado
    assert len(user.id) == 8  # Verifica se o ID gerado tem 8 caracteres

def test_check_password(test_client):
    user = User(name='Test User', email='test@example.com')
    user.set_password('my_secure_password')
    db.session.add(user)
    db.session.commit()
    
    assert user.check_password('my_secure_password') == True  # Senha correta
    assert user.check_password('wrong_password') == False     # Senha incorreta

def test_user_id_is_unique(test_client):
    user1 = User(name='Test User 1', email='test1@example.com')
    user1.set_password('password1')
    db.session.add(user1)
    db.session.commit()

    user2 = User(name='Test User 2', email='test2@example.com')
    user2.set_password('password2')
    db.session.add(user2)
    db.session.commit()

    assert user2.id != user1.id  # Verifica se os IDs são únicos

def test_password_hash_is_not_plain_text(test_client):
    user = User(name='Test User', email='test@example.com')
    user.set_password('my_secure_password')
    db.session.add(user)
    db.session.commit()
    
    assert user.password_hash != 'my_secure_password'  # Verifica se o hash não é igual à senha em texto puro
