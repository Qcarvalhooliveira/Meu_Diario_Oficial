import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    """
    Fixture to create and configure the Flask application for testing.
    
    This fixture sets up the Flask app in testing mode with a SQLite database.
    The app context is pushed, making the application accessible for the duration
    of the tests in this module.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/Meu_Diario_Oficial.db'
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_client(app):
    """
    Fixture to provide a test client for the Flask application.
    
    The test client allows for making requests to the application in a
    test context without running the server.
    """
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    """
    Fixture to initialize the database for testing.

    This fixture creates all the database tables before the tests in this module run,
    and drops them after the tests are complete. It ensures a clean database state
    for each test session.
    """
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
