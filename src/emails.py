from fastapi import APIRouter
from dotenv import load_dotenv
import resend
import os

load_dotenv()

router = APIRouter()

resend.api_key = os.getenv("RESEND_API_KEY")

params: resend.Emails.SendParams = {
    "from": "菇德 <good@camp.adk.to>",
    "to": ["ericchen08301@gmail.com"],
    "subject": "hello world",
    "html": "<p>it works!</p>",
}

# email = resend.Emails.send(params)
# print(email)


@router.get("/sample_endpoint")
def sample_endpoint():
    pass
