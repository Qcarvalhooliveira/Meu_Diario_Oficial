from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

# Initialize SQLAlchemy for database management
db = SQLAlchemy()

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate()

def create_app():
    """
    Factory function for creating and configuring the Flask application.
    """
    app = Flask(__name__)

    # Set secret key for session management and JWT
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Load configuration from the Config object
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Initialize Flask-Migrate with the app and database
    migrate.init_app(app, db)

    with app.app_context():
        # Import models to register them with SQLAlchemy
        from . import models
        
        # Create all database tables defined in models
        db.create_all()

        # Import and register the main blueprint
        from .views import main
        app.register_blueprint(main)

    return app
