import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///Meu_Diario_Oficial.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

