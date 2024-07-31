from . import db
from .models import User, Subscription
from .utils import download_pdf, extract_text_from_pdf
from .email import send_email
import time
from datetime import datetime

def process_daily_pdf():
    url = 'http://www.dom.salvador.ba.gov.br/'
    pdf_file = download_pdf(url)
    text = extract_text_from_pdf(pdf_file)

    subscriptions = Subscription.query.all()
    for sub in subscriptions:
        user = db.session.get(User, sub.user_id)
        if sub.keyword in text:
            send_notification(user.email, sub.keyword)

def send_notification(email, keyword):
    subject = "Parabéns! Seu nome foi encontrado no Diário Oficial"
    body = (
        f"Parabéns! '{keyword}',\n\n"
        "Seu nome foi encontrado no Diário Oficial de Salvador.\n\n"
        "Por favor, verifique diretamente no site para qual concurso você foi convocado.\n"
    )
    send_email(email, subject, body)

def should_run_today():
    today = datetime.today()
    # Verificar se é sábado (5) ou domingo (6)
    if today.weekday() >= 5:
        return False
    # Adicionar verificação de feriados (Bahia)
    holidays = [
        "01-01",  # Ano Novo
        "21-04",  # Tiradentes
        "01-05",  # Dia do Trabalhador
        "02-07",  # Independêcia da Bahia
        "07-09",  # Independência do Brasil
        "12-10",  # Nossa Senhora Aparecida
        "02-11",  # Finados
        "15-11",  # Proclamação da República
        "25-12",  # Natal
    ]
    if today.strftime("%d-%m") in holidays:
        return False
    return True

if __name__ == "__main__":
    while True:
        if should_run_today():
            process_daily_pdf()
        time.sleep(24 * 60 * 60)  # Executa uma vez por dia
