import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

load_dotenv()

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.getenv("BrevoEmailAPIKEY")

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)

async def send_email(recipient: str, subject: str, body: str):
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": recipient}],
        sender={
            "email": os.getenv("BREVO_SENDER_EMAIL"),
            "name": os.getenv("BREVO_SENDER_NAME"),
        },
        subject=subject,
        html_content=body,
    )

    try:
        api_instance.send_transac_email(email)
        print("✅ Email sent successfully")
    except ApiException as e:
        print("❌ Brevo Error:", e)
        raise
