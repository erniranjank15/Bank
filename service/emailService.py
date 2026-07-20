from fastapi_mail import FastMail, MessageSchema, MessageType
from routers.config import conf

async def send_email(recipient: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)