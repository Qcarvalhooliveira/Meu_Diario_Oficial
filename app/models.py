import string
import random
from . import db

def generate_random_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class User(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=generate_random_id)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    keyword = db.Column(db.String(100), nullable=True)
