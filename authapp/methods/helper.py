from django.core.mail import send_mail
from blog import settings

def sent_to_email(request, email , message):
    message = f"Salom, {email}.\n\n{message}"
    subject = "Confirmation code"
    address = email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [address])