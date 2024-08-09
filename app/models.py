import string
import random
from . import db
import bcrypt

def generate_random_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class User(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=generate_random_id)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Gera o hash da senha e o armazena."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
