from celery import shared_task
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .tokens import account_activation_token   # import your token generator

@shared_task
def send_activation_email(user_id: int, domain: str) -> None:
    """Asynchronously build and send the activation email."""
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    subject = "Activate Your MySite Account"
    message = render_to_string(
        "registration/account_activation_email.html",
        {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    user.email_user(subject, message)