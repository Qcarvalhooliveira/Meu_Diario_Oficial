from app import db, create_app
from app.models import User
import pytest


@pytest.fixture(scope='function')
def test_client():
    """
    Creates and configures a test client with an in-memory SQLite database.
    Ensures that a clean database is used for each test.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


def test_new_user(test_client):
    """
    Tests the creation of a new user in the database.
    Verifies that the user's attributes are correctly assigned and that a unique ID is generated.
    """
    user = User(name='Test User', email='test@example.com')
    user.set_password('my_secure_password')
    db.session.add(user)
    db.session.commit()
    
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'
    assert user.password_hash is not None  # Verifies that the password has been hashed
    assert user.id is not None  # Verifies that an ID has been generated
    assert len(user.id) == 8  # Verifies that the generated ID has 8 characters


def test_check_password(test_client):
    """
    Tests the password verification of a user.
    Verifies that the correct password is validated and that an incorrect password is rejected.
    """
    user = User(name='Test User', email='test@example.com')
    user.set_password('my_secure_password')
    db.session.add(user)
    db.session.commit()
    
    assert user.check_password('my_secure_password') == True
    assert user.check_password('wrong_password') == False


def test_user_id_is_unique(test_client):
    """
    Tests if the generated IDs for different users are unique.
    Verifies that two different users do not share the same ID.
    """
    user1 = User(name='Test User 1', email='test1@example.com')
    user1.set_password('password1')
    db.session.add(user1)
    db.session.commit()

    user2 = User(name='Test User 2', email='test2@example.com')
    user2.set_password('password2')
    db.session.add(user2)
    db.session.commit()

    assert user2.id != user1.id


def test_password_hash_is_not_plain_text(test_client):
    """
    Tests if the password stored in the database is properly hashed.
    """
    user = User(name='Test User', email='test@example.com')
    user.set_password('my_secure_password')
    db.session.add(user)
    db.session.commit()
    
    assert user.password_hash != 'my_secure_password'
