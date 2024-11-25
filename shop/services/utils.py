from django.core.mail import EmailMessage
from django.conf import settings

def send_email(subject, message, recipient_list, from_email=None, html=False):
    """
    Sends an email using Django's EmailMessage class.
    """
    if from_email is None:
        from_email = settings.EMAIL_HOST_USER # Replace with your email

    email = EmailMessage(subject, message, from_email, recipient_list)
    if html:
        email.content_subtype = "html"  # Set content to HTML
    email.send()



