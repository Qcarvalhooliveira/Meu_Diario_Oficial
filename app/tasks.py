from . import db
from .models import User
from .utils import download_pdf, extract_text_from_pdf
from .email import send_email
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_daily_pdf():
    url = 'http://www.dom.salvador.ba.gov.br/'
    pdf_file = download_pdf(url)
    text = extract_text_from_pdf(pdf_file)

    users = User.query.all()
    logger.info(f"Found {len(users)} users in the database")
    for user in users:
        if user.name and user.name in text:
            logger.info(f"Name '{user.name}' found for user {user.email}")
            send_notification(user.email, user.name)

def send_notification(email, name):
    subject = "Parabéns! Seu nome foi encontrado no Diário Oficial"
    body = (
        f"Parabéns! '{name}',\n\n"
        "Seu nome foi encontrado no Diário Oficial de Salvador.\n\n"
        "Por favor, verifique diretamente no site para qual concurso você foi convocado.\n"
    )
    send_email(email, subject, body)
    logger.info(f"Notification sent to {email} for name '{name}'")

def should_run_today():
    today = datetime.today()
    if today.weekday() >= 5:
        logger.info("Today is weekend, no need to run the task")
        return False
    holidays = [
        "01-01",
        "21-04",
        "01-05",
        "02-07",
        "07-09",
        "12-10",
        "02-11",
        "15-11",
        "25-12",
    ]
    if today.strftime("%d-%m") in holidays:
        logger.info("Today is a holiday, no need to run the task")
        return False
    return True

if __name__ == "__main__":
    while True:
        if should_run_today():
            process_daily_pdf()
        time.sleep(24 * 60 * 60)
