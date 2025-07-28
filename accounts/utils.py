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


def send_welcome_email(user):
    subject = "Welcome to Link Lovers!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    # Render the HTML template
    html_content = render_to_string('accounts/welcome-email.html', {'user': user})
    text_content = f"Hi {user.username},\n\nWelcome to Link Lovers. We're excited to have you on board!"  # Fallback plain text

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# def send_welcome_email(user):
#     subject = "Welcome to Ice Dating!"
#     message = f"Hi {user.username},\n\nWelcome to Test Dating. We're excited to have you on board!"
#     recipient_list = [user.email]
#
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
