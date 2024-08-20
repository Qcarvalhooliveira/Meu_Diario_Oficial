# tasks.py
from . import db
from .models import User
from .utils import download_pdf, extract_text_from_pdf
from .email import send_email, generate_notification_email, generate_error_email
import time
from datetime import datetime
import logging

# Configure logging for this module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for retry logic
MAX_RETRIES = 3
RETRY_INTERVAL = 60 * 60  # 1 hour

def process_daily_pdf():
    """
    Downloads the daily PDF from the official site, extracts text,
    and checks for user names. If a match is found, sends a notification
    email to the user. If the process fails, retries up to MAX_RETRIES times.
    If all retries fail, sends a failure notification to all users.
    """
    url = 'http://www.dom.salvador.ba.gov.br/'
    retries = 0
    success = False
    
    while retries < MAX_RETRIES and not success:
        try:
            pdf_file = download_pdf(url)
            if pdf_file:
            # Normalize the extracted text for easier matching
                text = extract_text_from_pdf(pdf_file)
                text_normalized = ' '.join(text.lower().split())
            # Fetch all users from the database
                users = User.query.all()
                logger.info(f"Found {len(users)} users in the database")
            # Check if any user's name appears in the text   
                for user in users:  
                    user_name_normalized = ' '.join(user.name.lower().split())
                    if user_name_normalized in text_normalized:
                        logger.info(f"Keyword '{user.name}' found for user {user.email}")
                        send_notification(user.email, user.name)
                success = True
        except Exception as e:
            logger.warning(f"Attempt {retries + 1} failed with error: {e}")
        # Log the failure and retry after a delay
        retries += 1
        if retries < MAX_RETRIES:
            time.sleep(RETRY_INTERVAL)
    
    if not success:
    # If all retries fail, notify users of the failure
        logger.error("Failed to process PDF after maximum retries")
        notify_failure()

def send_notification(email, keyword):
    """
    Sends a notification email to the user indicating that their name
    was found in the daily publication.
    """
    subject = "Parabéns! Seu nome foi encontrado no Diário Oficial"
    logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png" 
    body = generate_notification_email(keyword, logo_url)
    send_email(email, subject, body)
    logger.info(f"Notification sent to {email} for keyword '{keyword}'")

def notify_failure():
    """
    Sends an email to all users notifying them that the daily PDF
    processing failed after the maximum number of retries.
    """
    users = User.query.all()
    subject = "Falha na Verificação do Diário Oficial"
    logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png" 
    for user in users:
        body = generate_error_email(user.name, logo_url)
        send_email(user.email, subject, body)
        logger.info(f"Failure notification sent to {user.email}")

def should_run_today():
    """
    Determines whether the daily task should run today. The task is skipped
    if today is a weekend or a recognized holiday.
    """
    today = datetime.today()
    
    # Skip weekends
    if today.weekday() >= 5:
        logger.info("Today is weekend, no need to run the task")
        return False
    
    # List of holidays (MM-DD format)
    holidays = [
        "01-01",  # New Year's Day
        "21-04",  # Tiradentes' Day
        "01-05",  # Labor Day
        "02-07",  # Independence of Bahia
        "07-09",  # Independence Day
        "12-10",  # Our Lady of Aparecida
        "02-11",  # All Souls' Day
        "15-11",  # Republic Proclamation Day
        "25-12",  # Christmas
    ]
    
    # Skip recognized holidays
    if today.strftime("%d-%m") in holidays:
        logger.info("Today is a holiday, no need to run the task")
        return False
    
    return True

if __name__ == "__main__":
    """
    Main loop that runs the daily PDF processing task.
    The task checks whether it should run today, and if so,
    it attempts to process the PDF.
    """
    while True:
        if should_run_today():
            process_daily_pdf()
        # Wait 24 hours before the next run
        time.sleep(24 * 60 * 60)
