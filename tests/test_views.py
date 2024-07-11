import json
import pytest
from app import db, create_app
from app.models import User

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

@pytest.fixture(scope='module')
def init_database():
    user = User(name='Initial User', email='initial@example.com')
    db.session.add(user)
    db.session.commit()

    yield db  # Este yield retorna o banco de dados para uso nos testes

    db.drop_all()

def test_add_user(test_client, init_database):
    response = test_client.post('/add_user', 
                                data=json.dumps(dict(name='Test User', email='test@example.com')),
                                content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'User added successfully!'
    

def test_add_subscription(test_client, init_database):
    # Primeiro, adicionar um usuário único
    response = test_client.post('/add_user', 
                                data=json.dumps(dict(name='Subscription User', email='subscription@example.com')),
                                content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'User added successfully!'
    
    # Obter o user_id do novo usuário adicionado
    new_user = User.query.filter_by(email='subscription@example.com').first()
    user_id = new_user.id
    
    # Adicionar uma subscrição para o usuário
    response = test_client.post('/add_subscription', 
                                data=json.dumps(dict(user_id=user_id, keyword='test keyword')),
                                content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'Subscription added successfully!'
