# from django.db import models
# from django.contrib.auth.models import User
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField()
#     profile_picture = models.ImageField(upload_to='profile_pics')
#     # Add more fields as needed


from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics')
    # Add more fields as needed
