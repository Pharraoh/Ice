from django.utils import timezone
from datetime import timedelta
from .models import User  # Assuming you're using a custom User model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

def get_online_users(minutes=5):
    threshold = timezone.now() - timedelta(minutes=minutes)
    return User.objects.filter(last_seen__gte=threshold)


#smtp
# def send_welcome_email(user):
#     subject = "Welcome to Link Lovers!"
#     from_email = settings.DEFAULT_FROM_EMAIL
#     to = [user.email]
#
#     # Render the HTML template
#     html_content = render_to_string('accounts/welcome-email.html', {'user': user})
#     text_content = f"Hi {user.username},\n\nWelcome to Link Lovers. We're excited to have you on board!"  # Fallback plain text
#
#     msg = EmailMultiAlternatives(subject, text_content, from_email, to)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()


from django.template.loader import render_to_string
from .brevo import send_brevo_email

def send_welcome_email(user):
    subject = "Welcome to Link Lovers!"

    html_content = render_to_string(
        "accounts/welcome-email.html",
        {"user": user},
    )

    send_brevo_email(
        subject=subject,
        html_content=html_content,
        to_email=user.email,
        to_name=user.username,
    )




def send_password_reset_email(user, reset_link):
    subject = "Password Reset Request"

    html_content = render_to_string(
        "accounts/password_reset_email.html",
        {
            "user": user,
            "reset_link": reset_link,
        },
    )

    send_brevo_email(
        subject=subject,
        html_content=html_content,
        to_email=user.email,
        to_name=user.username,
    )
