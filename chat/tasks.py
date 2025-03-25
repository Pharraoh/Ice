from celery import shared_task
from django.utils import timezone
from .models import Status

@shared_task
def delete_expired_statuses():
    now = timezone.now()
    expired_statuses = Status.objects.filter(created_at__lte=now - timezone.timedelta(hours=24))
    count = expired_statuses.count()
    expired_statuses.delete()
    return f"Deleted {count} expired statuses"
