from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

print("MAIL_SERVER:", os.getenv("MAIL_SERVER"))
print("MAIL_PORT:", os.getenv("MAIL_PORT"))
print("MAIL_STARTTLS:", os.getenv("MAIL_STARTTLS"))
print("MAIL_SSL_TLS:", os.getenv("MAIL_SSL_TLS"))
print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
print("MAIL_PASSWORD exists:", bool(os.getenv("MAIL_PASSWORD")))

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS"),
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS"),
    USE_CREDENTIALS=True
)