from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.tasks import process_daily_pdf, should_run_today
import atexit
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

# Configuration for APScheduler
scheduler = BackgroundScheduler()

def scheduled_task():
    if should_run_today():
        with app.app_context():
            logger.info("Running scheduled task")
            process_daily_pdf()

# Schedule the task to run every day at 12:50
scheduler.add_job(func=scheduled_task, trigger=CronTrigger(hour=20, minute=5))

scheduler.start()

# Shut down the scheduler when the application exits
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(debug=False)