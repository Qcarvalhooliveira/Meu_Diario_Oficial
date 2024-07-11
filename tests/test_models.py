from app import db, create_app
from app.models import User, Subscription
import pytest

@pytest.fixture(scope='module')
def new_user():
    user = User(name='Test User', email='test@example.com')
    return user

@pytest.fixture(scope='module')
def new_subscription(new_user):
    subscription = Subscription(user_id=new_user.id, keyword='test keyword')
    return subscription

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

def test_new_subscription(new_subscription):
    assert new_subscription.keyword == 'test keyword'
