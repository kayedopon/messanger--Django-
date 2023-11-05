from django.conf import settings
from django.template import Context
from django.dispatch import receiver, Signal
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.signing import TimestampSigner
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string, get_template
from datetime import timedelta


User = get_user_model()

user_registered = Signal()

@receiver(user_registered, sender=User)
def user_post_register_reciever(sender, instance, *args, **kwargs):
    token_expiration = int((timezone.now() + timedelta(seconds=30)).timestamp())
    data = {
        "username": instance.username,
        "email": instance.email,
        "token_expiration": token_expiration,
    }
    registration_token = generate_signed_token(data)
    data["registration_token"] = registration_token
    
    send_verification_email(data)


def generate_signed_token(data: dict):
    signer = TimestampSigner()
    token = signer.sign_object(data)
    return token

def send_verification_email(data: dict):
    html_message = render_to_string('main/email_template.html', context=data)
    plain_message = strip_tags(html_message)
    # message = get_template('main/email_template.html').render(Context(data))
    email = EmailMultiAlternatives(
        "Email Verification",
        plain_message,
        settings.EMAIL_HOST_USER,
        [data['email']],
    )
    email.attach_alternative(html_message, "text/html")
    email.fail_silently = False
    email.send()