import pytest
from app import create_app, db
from app.models import User
from flask import url_for

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
        user1.set_password('password1')
        user2 = User(name='Test User 2', email='iurithauront@gmail.com')
        user2.set_password('password2')
        db.session.add_all([user1, user2])
        db.session.commit()

        yield db
        db.session.remove()
        db.drop_all()

def test_add_user(test_client):
    response = test_client.post('/add_user', json={
        'name': 'Test User 3',
        'email': 'testuser3@example.com',
        'password': 'password3'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'User added successfully!'
    assert User.query.filter_by(email='testuser3@example.com').first() is not None

def test_login(test_client, init_database):
    response = test_client.post('/login', json={
        'email': 'queisecarvalho@hotmail.com',
        'password': 'password1'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert 'token' in data

    # Teste de falha de login
    response = test_client.post('/login', json={
        'email': 'queisecarvalho@hotmail.com',
        'password': 'wrongpassword'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == 'Email ou senha incorretos!'

def test_delete_user(test_client, init_database):
    # Primeiro, faça login para obter o token
    login_response = test_client.post('/login', json={
        'email': 'queisecarvalho@hotmail.com',
        'password': 'password1'
    })
    token = login_response.get_json()['token']

    # Tente excluir o usuário usando o token
    user = User.query.filter_by(email='queisecarvalho@hotmail.com').first()
    response = test_client.delete(f'/delete_user/{user.id}', headers={
        'Authorization': f'Bearer {token}'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'User deleted successfully!'
    assert db.session.get(User, user.id) is None

def test_get_users(test_client, init_database):
    response = test_client.get('/users')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) > 0  # Verifica se a lista de usuários não está vazia

if __name__ == "__main__":
    pytest.main()
