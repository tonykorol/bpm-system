import smtplib
from email.mime.text import MIMEText

from src.config import settings


def send_email(email: str, subject: str, body: str):
    """Send an email using SMTP.

    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Sends the email through an SMTP server configured in the application settings.
    The SMTP server connection is secured using SSL, and login credentials are provided for authentication.

    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = email

    with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(settings.SMTP_USER, email, msg.as_string())
