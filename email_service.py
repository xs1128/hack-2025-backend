from dotenv import load_dotenv
import resend

import os

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")
params: resend.Emails.SendParams = {
  "from": "菇德 <good@camp.adk.to>",
  "to": ["ericchen08301@gmail.com"],
  "subject": "hello world",
  "html": "<p>it works!</p>"
}

email = resend.Emails.send(params)
print(email)