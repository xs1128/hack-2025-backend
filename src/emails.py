import time
import threading
from datetime import datetime
from fastapi import APIRouter
from dotenv import load_dotenv
import resend
import os
from email_contents import EMAIL_REMINDER_LIST, EMAIL_FIXED_LIST
from shared_data import users

load_dotenv()
router = APIRouter()
resend.api_key = os.getenv("RESEND_API_KEY")

# Define your email sending times (24-hour format)
EMAIL_TIMES = ["21:00", "21:30", "22:00", "22:30", "23:00"]


@router.get("/send-email")
def send_email():
    """Function to send your email"""
    if len(users) > 0:
        params: resend.Emails.SendParams = {
            "from": "菇德 <good@camp.adk.to>",
            # TODO: use id instead of hard code 0 index
            "to": users[0]["email"],
            "subject": "EMAIL_FIXED_LIST[0]['subject']",
            "html": "<p>it works!</p>"
        }

        try:
            email = resend.Emails.send(params)
            print(f"Email sent at {
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return email
        except Exception as e:
            print(f"Failed to send email: {e}")


def email_scheduler():
    """Main scheduler function that runs continuously"""
    print("Email scheduler started...")
    print(f"Will send emails at: {', '.join(EMAIL_TIMES)}")

    last_sent_minute = None

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # Only send once per minute to avoid duplicates
        if current_time in EMAIL_TIMES and current_time != last_sent_minute:
            send_email()
            last_sent_minute = current_time

        # Check every 30 seconds
        time.sleep(30)


# Start the scheduler immediately when this module is imported
scheduler_thread = threading.Thread(target=email_scheduler, daemon=True)
scheduler_thread.start()
