from . import db
from .models import User, Subscription
from .utils import download_pdf, extract_text_from_pdf
from .email import send_email
import time

def process_daily_pdf():
    url = 'http://www.dom.salvador.ba.gov.br/'  # Substitua pela URL correta
    pdf_file = download_pdf(url)
    text = extract_text_from_pdf(pdf_file)

    subscriptions = Subscription.query.all()
    for sub in subscriptions:
        user = db.session.get(User, sub.user_id)
        if sub.keyword in text:
            send_notification(user.email, sub.keyword)

def send_notification(email, keyword):
    subject = "Notificação de Palavra-chave"
    body = f"Sua palavra-chave '{keyword}' foi encontrada no DOU."
    send_email(email, subject, body)

if __name__ == "__main__":
    while True:
        process_daily_pdf()
        time.sleep(24 * 60 * 60)  # Executa uma vez por dia
