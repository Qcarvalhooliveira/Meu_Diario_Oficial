import pytest
from unittest.mock import patch
from app.models import User, Subscription
from app.tasks import process_daily_pdf, send_notification
from app import db, create_app

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
def init_database(test_client):
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

def test_process_daily_pdf(init_database):
    with patch('app.tasks.download_pdf') as mock_download_pdf, \
         patch('app.tasks.extract_text_from_pdf') as mock_extract_text_from_pdf, \
         patch('app.tasks.send_notification') as mock_send_notification:

        mock_download_pdf.return_value = b"%PDF-1.4..."
        mock_extract_text_from_pdf.return_value = "This is a test document with test keyword 1 and some more text."

        process_daily_pdf()

        mock_send_notification.assert_called_once_with('queisecarvalho@hotmail.com', 'test keyword 1')
        assert mock_send_notification.call_count == 1

def test_send_notification():
    with patch('app.email.send_email') as mock_send_email:
        send_notification('queisecarvalho@hotmail.com', 'test keyword 1')
        
        mock_send_email.assert_called_once()
        args, kwargs = mock_send_email.call_args
        recipient, subject, body = args

        assert recipient == 'queisecarvalho@hotmail.com'
        assert subject == "Notificação de Palavra-chave"
        assert body == "Sua palavra-chave 'test keyword 1' foi encontrada no DOU."
