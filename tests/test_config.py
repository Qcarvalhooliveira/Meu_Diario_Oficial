from app import create_app

def test_config():
    """
    Test to verify the application configuration settings.
    
    This test ensures that the `SQLALCHEMY_TRACK_MODIFICATIONS` configuration
    option is set to `False`, as expected. This setting is recommended to be
    disabled to avoid significant overhead when working with a large number of
    database operations.
    """
    app = create_app()
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
