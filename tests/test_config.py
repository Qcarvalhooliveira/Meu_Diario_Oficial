from app import create_app

def test_config():
    app = create_app()
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
