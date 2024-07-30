import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do .env

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/Meu_Diario_Oficial.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'seu_email@example.com')
