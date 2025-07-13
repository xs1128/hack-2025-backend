import time
import threading
import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Response
from dotenv import load_dotenv
import resend
import os
from email_contents import EMAIL_REMINDER_LIST, EMAIL_FIXED_LIST
from shared_data import users

load_dotenv()
router = APIRouter()
resend.api_key = os.getenv("RESEND_API_KEY")


@router.get("/internal/morning-mail")
def send_morning_email():

    if len(users) == 0:
        print("No users available to send morning email")
        return None

    if len(EMAIL_FIXED_LIST) == 0:
        raise ValueError(
            "EMAIL_FIXED_LIST is empty. Please check your email content configuration."
        )

    email_content = random.choice(EMAIL_FIXED_LIST)

    for user in users:
        params: resend.Emails.SendParams = {
            "from": "菇德 <good@camp.adk.to>",
            "to": user["email"],
            "subject": email_content["subject"],
            "html": email_content["html"],
        }

        resend.Emails.send(params)
    return Response(status_code=204)


@router.get("/internal/night-mail")
def send_reminder_email():

    if len(users) == 0:
        print("No users available to send reminder email")
        return None

    if len(EMAIL_REMINDER_LIST) == 0:
        print("No reminder email content available")
        return None
    email_content = random.choice(EMAIL_REMINDER_LIST)
    for user in users:
        if (
            user["quiz"]["last_played"]
            and user["quiz"]["last_played"].date() == datetime.now().date()
        ):
            continue
        params: resend.Emails.SendParams = {
            "from": "菇德 <good@camp.adk.to>",
            "to": user["email"],
            "subject": "姑德的溫馨提醒",
            "html": f"<p>{email_content}</p>",
        }

        resend.Emails.send(params)

    return Response(status_code=204)
