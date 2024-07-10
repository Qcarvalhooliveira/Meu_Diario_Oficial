from . import db
from .models import User, Subscription
from .utils import download_pdf, extract_text_from_pdf
import time

def process_daily_pdf():
    url = 'http://www.dom.salvador.ba.gov.br/'  # Substitua pela URL correta
    pdf_file = download_pdf(url)
    text = extract_text_from_pdf(pdf_file)

    subscriptions = Subscription.query.all()
    for sub in subscriptions:
        if sub.keyword in text:
            user = User.query.get(sub.user_id)
            send_notification(user.email, sub.keyword)

def send_notification(email, keyword):
    # Função para enviar email de notificação
    print(f"Enviando notificação para {email} sobre {keyword}")

if __name__ == "__main__":
    while True:
        process_daily_pdf()
        time.sleep(24 * 60 * 60)  # Executa uma vez por dia