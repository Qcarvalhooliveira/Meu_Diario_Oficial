import pytest
from unittest.mock import patch
from app.models import User
from app.tasks import process_daily_pdf, send_notification, should_run_today
from app import db, create_app
from datetime import datetime
@pytest.fixture(scope='function')
def init_database(test_client):
    """
    Initializes the database with test users for each test.
    Cleans up the database after each test.
    """
    with test_client.application.app_context():
        db.create_all()  # Create the tables in the database

        # Add test users to the database
        user1 = User(name='Test User 1', email='testuser1@example.com')
        user1.set_password('password1')
        db.session.add(user1)
        db.session.commit()

        yield db  # This is where the testing happens!

        # Clean up the database after the test is done
        db.session.remove()
        db.drop_all()

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

def test_process_daily_pdf_success(init_database):
    """
    Tests the successful processing of the daily PDF.
    Mocks the PDF download and extraction process, and verifies that notifications are sent correctly.
    """
    with patch('app.tasks.download_pdf') as mock_download_pdf, \
         patch('app.tasks.extract_text_from_pdf') as mock_extract_text_from_pdf, \
         patch('app.tasks.send_notification') as mock_send_notification, \
         patch('time.sleep', return_value=None):  # Mock time.sleep to prevent delays

        # Mock the download and extraction of the PDF
        mock_download_pdf.return_value = b"%PDF-1.4..."
        mock_extract_text_from_pdf.return_value = "This is a test document with Test User 1 and some more text."

        # Run the process_daily_pdf function
        process_daily_pdf()

        # Verify that the notification was sent correctly
        mock_send_notification.assert_called_once_with('testuser1@example.com', 'Test User 1')
        assert mock_send_notification.call_count == 1
def test_process_daily_pdf_multiple_users(init_database):
    """
    Tests the processing of the daily PDF with multiple users.
    Verifies that notifications are sent to the correct users based on the PDF content.
    """
    with patch('app.tasks.download_pdf') as mock_download_pdf, \
         patch('app.tasks.extract_text_from_pdf') as mock_extract_text_from_pdf, \
         patch('app.tasks.send_notification') as mock_send_notification, \
         patch('time.sleep', return_value=None):  # Mock time.sleep to prevent delays

        # Add additional users to the database
        user2 = User(name='Test User 2', email='testuser2@example.com')
        user2.set_password('password2')
        user3 = User(name='User No Match', email='nomatch@example.com')
        user3.set_password('password3')
        db.session.add_all([user2, user3])
        db.session.commit()

        # Mock the download and extraction of the PDF
        mock_download_pdf.return_value = b"%PDF-1.4..."
        mock_extract_text_from_pdf.return_value = (
            "This is a test document with Test User 1 and Test User 2."
        )

        # Run the process_daily_pdf function
        process_daily_pdf()

        # Verify that notifications were sent to the correct users
        mock_send_notification.assert_any_call('testuser1@example.com', 'Test User 1')
        mock_send_notification.assert_any_call('testuser2@example.com', 'Test User 2')
        assert mock_send_notification.call_count == 2  # Should be called twice, not for User No Match

def test_process_daily_pdf_failure(init_database):
    """
    Tests the scenario where the PDF processing fails after maximum retries.
    Verifies that the failure notification is sent to all users.
    """
    with patch('app.tasks.download_pdf', return_value=None) as mock_download_pdf, \
         patch('app.tasks.notify_failure') as mock_notify_failure, \
         patch('time.sleep', return_value=None):  # Mock time.sleep to avoid delays

        # Run the process_daily_pdf function, expecting it to fail
        process_daily_pdf()

        # Verify that notify_failure is called once after retries
        mock_notify_failure.assert_called_once()
        assert mock_notify_failure.call_count == 1


@pytest.mark.parametrize("date_str, expected", [
    ("2024-07-26", True),  # Sexta-feira
    ("2024-07-27", False),  # Sábado
    ("2024-07-28", False),  # Domingo
    ("2024-01-01", False),  # Ano Novo
    ("2024-04-21", False),  # Tiradentes
    ("2024-05-01", False),  # Dia do Trabalho
    ("2024-07-02", False),  # Independência da Bahia
    ("2024-09-07", False),  # Independência do Brasil
    ("2024-10-12", False),  # Nossa Senhora Aparecida
    ("2024-11-02", False),  # Finados
    ("2024-11-15", False),  # Proclamação da República
    ("2024-12-25", False),  # Natal
    ("2024-08-20", True),   # Dia útil, não é feriado
])
def test_should_run_today(monkeypatch, date_str, expected):
    """
    Tests whether the task should run on the given date.
    Uses parameterized testing to check different dates including weekends and holidays.
    """
    # Mocking datetime to control the current date
    class MockDateTime(datetime):
        @classmethod
        def today(cls):
            return cls.strptime(date_str, "%Y-%m-%d")

    # Mock datetime.today() to return the mocked date
    with patch('app.tasks.datetime', MockDateTime):
        assert should_run_today() == expected


if __name__ == "__main__":
    pytest.main()
