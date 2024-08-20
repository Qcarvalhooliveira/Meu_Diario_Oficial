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
