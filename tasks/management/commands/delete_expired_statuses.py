from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from chat.models import Status

class Command(BaseCommand):
    help = "Delete statuses older than 24 hours"

    def handle(self, *args, **kwargs):
        expiry_time = now() - timedelta(hours=24)
        deleted_count, _ = Status.objects.filter(created_at__lt=expiry_time).delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Deleted {deleted_count} expired statuses"))
