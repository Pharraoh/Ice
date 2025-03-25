# from django.db import models
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# class ChatRoom(models.Model):
#     participants = models.ManyToManyField(User, related_name='chatrooms')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"ChatRoom {self.id} - Participants: {', '.join(user.username for user in self.participants.all())}"
#
#
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"From {self.sender.username} to {self.receiver.username}: {self.content[:20]}"
from django.conf import settings
from django.db import models

class ChatRoom(models.Model):
    # A unique room for two users
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="room_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="room_user2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"

    def room_name(self):
        return f"room_{min(self.user1.id, self.user2.id)}_{max(self.user1.id, self.user2.id)}"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}"



from django.contrib.auth import get_user_model

User = get_user_model()



from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Status(models.Model):
    STATUS_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="statuses")
    status_type = models.CharField(max_length=10, choices=STATUS_TYPES)
    text = models.TextField(blank=True, null=True)  # For text statuses
    media = models.FileField(upload_to="statuses/", blank=True, null=True)  # For images/videos
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.user.username} - {self.status_type} ({self.created_at})"

    def is_expired(self):
        return self.created_at < now() - timedelta(hours=24)  # ✅ Check if 24 hours have passed
