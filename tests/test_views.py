import pytest
from app import create_app, db
from app.models import User, Subscription

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/Meu_Diario_Oficial.db'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.create_all()
        user1 = User(name='Test User 1', email='queisecarvalho@hotmail.com')
        user2 = User(name='Test User 2', email='iurithauront@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        subscription1 = Subscription(user_id=user1.id, keyword='test keyword 1')
        subscription2 = Subscription(user_id=user2.id, keyword='test keyword 2')
        db.session.add(subscription1)
        db.session.add(subscription2)
        db.session.commit()

        yield db
        db.session.remove()
        db.drop_all()

def test_add_user(test_client):
    response = test_client.post('/add_user', json={
        'name': 'Test User 3',
        'email': 'testuser3@example.com'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'User added successfully!'
    assert User.query.filter_by(email='testuser3@example.com').first() is not None

def test_add_subscription(test_client, init_database):
    user = User.query.filter_by(email='queisecarvalho@hotmail.com').first()
    response = test_client.post('/add_subscription', json={
        'user_id': user.id,
        'keyword': 'new keyword'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Subscription added successfully!'
    assert Subscription.query.filter_by(user_id=user.id, keyword='new keyword').first() is not None

def test_delete_user(test_client, init_database):
    user = User.query.filter_by(email='queisecarvalho@hotmail.com').first()
    response = test_client.delete(f'/delete_user/{user.id}')
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'User and associated subscriptions deleted successfully!'
    assert User.query.get(user.id) is None
    assert Subscription.query.filter_by(user_id=user.id).count() == 0

if __name__ == "__main__":
    pytest.main()
