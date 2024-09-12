from datetime import datetime,timezone
import string
import random
from . import db
import bcrypt

def generate_random_id(length=8):
    """
    Generates a random alphanumeric ID of the specified length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class User(db.Model):
    """
    User model representing a user in the application.
    """
    id = db.Column(db.String(50), primary_key=True, default=generate_random_id)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    selections = db.relationship('UserSelection', backref='user', lazy=True)

    def set_password(self, password):
        """
        Generates a hashed version of the provided password and stores it.
        """
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """
        Verifies if the provided password matches the stored hashed password.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class UserSelection(db.Model):
    """
    Model to track when a user was selected.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    selected_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<UserSelection {self.user_id} - {self.selected_at}>'