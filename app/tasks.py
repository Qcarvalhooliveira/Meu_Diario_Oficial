import requests
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
    print("Starting process_daily_pdf...")
    url = 'http://www.dom.salvador.ba.gov.br/'
    retries = 0
    success = False
    
    while retries < MAX_RETRIES and not success:
        try:
            print(f"Attempt {retries + 1} to download and process PDF...")
            pdf_file = download_pdf(url)
            if pdf_file:
                print("PDF downloaded successfully.")
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
                break
            else:
                print("PDF file is None.")
        except Exception as e:
            logger.warning(f"Attempt {retries + 1} failed with error: {e}")
            print(f"Exception occurred: {e}")
        # Log the failure and retry after a delay
        retries += 1
        if retries < MAX_RETRIES:
            print(f"Retrying in {RETRY_INTERVAL} seconds...")
            time.sleep(RETRY_INTERVAL)
    
    if not success:
        # If all retries fail, notify users of the failure
        logger.error("Failed to process PDF after maximum retries")
        print("All retries failed. Notifying users of the failure.")
        notify_failure()

def send_notification(email, keyword):
    """
    Sends a notification email to the user indicating that their name
    was found in the daily publication.
    """
    print(f"Sending notification to {email} for keyword '{keyword}'...")

    subject = "Parabéns! Seu nome foi encontrado no Diário Oficial"
    logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png" 
    body = generate_notification_email(keyword, logo_url)
    send_email(email, subject, body)
    logger.info(f"Notification sent to {email} for keyword '{keyword}'")
    print(f"Notification sent to {email}.")

    user = User.query.filter_by(email=email).first()
    if user:
        try:
            response = requests.post(f'http://127.0.0.1:5000/select_user/{user.id}')
            if response.status_code == 200:
                logger.info(f"User selection registered for {user.name} (ID: {user.id})")
            else:
                logger.error(f"Failed to register selection for {user.name} (ID: {user.id}). Status code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error registering user selection for {user.name}: {e}")

def notify_failure():
    """
    Sends an email to all users notifying them that the daily PDF
    processing failed after the maximum number of retries.
    """
    print("Sending failure notifications to all users...")
    users = User.query.all()
    subject = "Falha na Verificação do Diário Oficial"
    logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png" 
    for user in users:
        body = generate_error_email(user.name, logo_url)
        send_email(user.email, subject, body)
        logger.info(f"Failure notification sent to {user.email}")
        print(f"Failure notification sent to {user.email}.")

def should_run_today():
    """
    Determines whether the daily task should run today. The task is skipped
    if today is a weekend or a recognized holiday.
    """
    print("Checking if the task should run today...")
    today = datetime.today()
    
    # Skip weekends
    if today.weekday() >= 5:
        logger.info("Today is weekend, no need to run the task")
        print("Today is a weekend. Skipping the task.")
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
        print("Today is a holiday. Skipping the task.")
        return False
    
    print("The task will run today.")
    return True

if __name__ == "__main__":
    """
    Main loop that runs the daily PDF processing task.
    The task checks whether it should run today, and if so,
    it attempts to process the PDF.
    """
    print("Starting main loop for daily PDF processing...")
    while True:
        if should_run_today():
            process_daily_pdf()
        # Wait 24 hours before the next run
        print("Sleeping for 24 hours...")
        time.sleep(24 * 60 * 60)