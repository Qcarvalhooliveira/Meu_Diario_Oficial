import pytest
from unittest.mock import patch
from app.models import User
from app.tasks import process_daily_pdf, send_notification, should_run_today
from app import db, create_app
from datetime import datetime

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/Meu_Diario_Oficial.db'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='function')
def init_database(test_client):
    with test_client.application.app_context():
        db.create_all()
        user1 = User(name='Test User 1', email='queisecarvalho@hotmail.com')
        user1.set_password('password1')
        user2 = User(name='Test User 2', email='iurithauront@gmail.com')
        user2.set_password('password2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        yield db
        db.session.remove()
        db.drop_all()

def test_process_daily_pdf(init_database):
    with patch('app.tasks.download_pdf') as mock_download_pdf, \
         patch('app.tasks.extract_text_from_pdf') as mock_extract_text_from_pdf, \
         patch('app.tasks.send_notification') as mock_send_notification:

        mock_download_pdf.return_value = b"%PDF-1.4..."
        mock_extract_text_from_pdf.return_value = "This is a test document with Test User 1 and some more text."

        process_daily_pdf()

        mock_send_notification.assert_called_once_with('queisecarvalho@hotmail.com', 'Test User 1')
        assert mock_send_notification.call_count == 1

       

@pytest.mark.parametrize("date_str, expected", [
    ("2024-07-26", True),  # Sexta-feira, não é feriado
    ("2024-07-27", False),  # Sábado
    ("2024-07-28", False),  # Domingo
    ("2024-01-01", False),  # Ano Novo
    ("2024-12-25", False),  # Natal
])
def test_should_run_today(monkeypatch, date_str, expected):
    # Mock datetime to control the current date
    class MockDateTime(datetime):
        @classmethod
        def today(cls):
            return cls.strptime(date_str, "%Y-%m-%d")

    monkeypatch.setattr("app.tasks.datetime", MockDateTime)
    assert should_run_today() == expected

if __name__ == "__main__":
    pytest.main()
