from django.conf import settings
from email.message import EmailMessage
import ssl
import smtplib


def send_email(receiver, port, subject, body, html=False):
    """
    Sends an email using SMTP.

    Args:
        receiver (str): The recipient email address.
        port (int): Port number for SMTP.
        subject (str): The email subject.
        body (str): The email body.
        html (bool): Whether the email content is in HTML.
    """
    em = EmailMessage()
    em['From'] = settings.EMAIL_HOST_USER
    em['To'] = receiver
    em['Subject'] = subject

    if html:
        em.add_alternative(body, subtype='html')
    else:
        em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST, port, context=context) as smtp:
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.sendmail(settings.EMAIL_HOST_USER, receiver, em.as_string())
