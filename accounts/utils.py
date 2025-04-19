from django.utils import timezone
from datetime import timedelta
from .models import User  # Assuming you're using a custom User model

def get_online_users(minutes=5):
    threshold = timezone.now() - timedelta(minutes=minutes)
    return User.objects.filter(last_seen__gte=threshold)
