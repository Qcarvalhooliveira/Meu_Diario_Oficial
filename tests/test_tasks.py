import pytest
from unittest.mock import patch
from app.models import User
from app.tasks import process_daily_pdf, send_notification, should_run_today, notify_failure
from app import db, create_app
from datetime import datetime


@pytest.fixture(scope='module')
def test_client():
    """
    Creates and configures a test client with an SQLite database for testing.
    Ensures a clean environment for each test run.
    """
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
    """
    Initializes the database with test users for each test.
    Cleans up the database after each test.
    """
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

def test_process_daily_pdf_success(init_database):
    """
    Tests the successful processing of the daily PDF.
    Mocks the PDF download and extraction process, and verifies that notifications are sent correctly.
    """
    with patch('app.tasks.download_pdf') as mock_download_pdf, \
         patch('app.tasks.extract_text_from_pdf') as mock_extract_text_from_pdf, \
         patch('app.tasks.send_notification') as mock_send_notification:

        # Mock the download and extraction of the PDF
        mock_download_pdf.return_value = b"%PDF-1.4..."
        mock_extract_text_from_pdf.return_value = "This is a test document with Test User 1 and some more text."

        process_daily_pdf()

        # Verify that the notification was sent correctly
        mock_send_notification.assert_called_once_with('queisecarvalho@hotmail.com', 'Test User 1')
        assert mock_send_notification.call_count == 1

def test_send_notification(init_database):
    """
    Tests the send_notification function to ensure it sends an email with the correct content.
    """
    with patch('app.email.send_email') as mock_send_email:
        send_notification('test@example.com', 'Test User')

        mock_send_email.assert_called_once_with(
            'test@example.com',
            "Parabéns! Seu nome foi encontrado no Diário Oficial",
            '<html><body style="background-color: #ffff; font-family: Arial, sans-serif; margin: 0; padding: 0; width: 100%;">'
            '<div style="background-color: #c7e6fd; padding: 20px; text-align: center;">'
            '<table align="center" width="100%" style="max-width: 600px; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">'
            '<tr><td style="text-align: center;">'
            '<img src="http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png" alt="Logo" style="margin: 0 0 30px 5px">'
            '<h1 style="color: #333333; text-align: left; font-size: 20px; margin: 5px 0;">Parabéns, Test User!</h1>'
            '<p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">Seu nome foi encontrado no Diário Oficial de Salvador!</p>'
            '<p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">Por favor, verifique diretamente no site para qual concurso você foi convocado.</p>'
            '<p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">Estamos torcendo por você!</p>'
            '</td></tr></table></div></body></html>'
        )

def test_process_daily_pdf_failure(init_database):
    """
    Tests the scenario where the PDF processing fails after maximum retries.
    Verifies that the failure notification is sent to all users.
    """
    with patch('app.tasks.download_pdf') as mock_download_pdf, \
         patch('app.tasks.notify_failure') as mock_notify_failure:

        # Mock the download_pdf to always return None (simulating failure)
        mock_download_pdf.return_value = None

        process_daily_pdf()

        # Verify that notify_failure is called once after retries
        mock_notify_failure.assert_called_once()
        assert mock_notify_failure.call_count == 1

@pytest.mark.parametrize("date_str, expected", [
    ("2024-07-26", True),  # Friday, not a holiday
    ("2024-07-27", False),  # Saturday
    ("2024-07-28", False),  # Sunday
    ("2024-01-01", False),  # New Year's Day
    ("2024-12-25", False),  # Christmas
])
def test_should_run_today(monkeypatch, date_str, expected):
    """
    Tests whether the task should run on the given date.
    Uses parameterized testing to check different dates including weekends and holidays.
    """
    class MockDateTime(datetime):
        @classmethod
        def today(cls):
            return cls.strptime(date_str, "%Y-%m-%d")

    # Mock datetime to control the current date
    monkeypatch.setattr("app.tasks.datetime", MockDateTime)
    assert should_run_today() == expected


if __name__ == "__main__":
    pytest.main()
