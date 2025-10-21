from django.conf import settings
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    room_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:20]}"



# status implementation
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

User = get_user_model()


import uuid
from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Status(models.Model):
    STATUS_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="realtime_statuses")
    status_type = models.CharField(max_length=10, choices=STATUS_TYPES)
    text = models.TextField(blank=True, null=True)  # For text statuses
    # media = CloudinaryField('media', resource_type='video', null=True)
    # media = models.FileField(upload_to="statuses/", blank=True, null=True)  # For images/videos
    image = CloudinaryField('image', resource_type='image', blank=True, null=True)
    video = CloudinaryField('video', resource_type='video', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    caption = models.CharField(max_length=100, blank=True, null=True)  # ✅ For image/video captions


    @property
    def media_url(self):
        return self.image.url if self.status_type == 'image' else self.video.url if self.status_type == 'video' else None

    def __str__(self):
        return f"{self.user.username} - {self.status_type} ({self.created_at})"

    def is_expired(self):
        return self.created_at < now() - timedelta(hours=24)  # ✅ Check if 24 hours have passed
