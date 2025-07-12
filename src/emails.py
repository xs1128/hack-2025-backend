from fastapi import APIRouter
from dotenv import load_dotenv
import resend
import os
from apscheduler.schedulers.background import BackgroundScheduler
import random
from .email_contents import EMAIL_REMINDER_LIST, EMAIL_FIXED_LIST

load_dotenv()

router = APIRouter()
resend.api_key = os.getenv("RESEND_API_KEY")

def send_email(to: str, subject: str, html: str):
    params = resend.Emails.SendParams(
        **{
            "from": "菇德 <good@camp.adk.to>",
            "to": [to],
            "subject": subject,
            "html": html,
        }
    )
    try:
        email = resend.Emails.send(params)
        return email
    except Exception as e:
        print(f"Email send failed: {e}")
        return None

# Internal API: 傳固定 Email
@router.post("/internal/send_fixed_email")
def send_fixed_email(user_email: str):
    content = random.choice(EMAIL_FIXED_LIST)
    subject = "SITCON Camp 每日提醒"
    html = f"<p>{content}</p>"
    return send_email(user_email, subject, html)

# Internal API: 傳還沒做提醒 Email
@router.post("/internal/send_reminder_email")
def send_reminder_email(user_email: str):
    content = random.choice(EMAIL_REMINDER_LIST)
    subject = "SITCON Camp 還沒完成提醒"
    html = f"<p>{content}</p>"
    return send_email(user_email, subject, html)

# 定時任務
def schedule_emails():
    scheduler = BackgroundScheduler()
    # 9:00 定時發送
    scheduler.add_job(
        lambda: send_fixed_email("ericchen08301@gmail.com"),
        'cron', hour=9, minute=0, id='fixed_email_job'
    )
    # 22:30-23:59 每半小時發送一次提醒
    for minute in range(30, 60, 30):
        scheduler.add_job(
            lambda: send_reminder_email("ericchen08301@gmail.com"),
            'cron', hour=22, minute=minute, id=f'reminder_22_{minute}'
        )
    for minute in range(0, 60, 30):
        scheduler.add_job(
            lambda: send_reminder_email("ericchen08301@gmail.com"),
            'cron', hour=23, minute=minute, id=f'reminder_23_{minute}'
        )
    scheduler.start()

# 啟動時啟動排程
schedule_emails()
