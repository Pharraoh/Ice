from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class LGA(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="lgas")

    def __str__(self):
        return f"{self.name} ({self.state.name})"

class College(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class GradYear(models.Model):
    year = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.year



class User(AbstractUser):
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    email = models.EmailField(unique=True)  # ✅ Enforce unique emails
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    looking_for = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    birthday = models.DateField(max_length=10, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    lga = models.ForeignKey(LGA, on_delete=models.SET_NULL, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    grad_year = models.ForeignKey(GradYear, on_delete=models.SET_NULL, null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='single')
    bio = models.TextField(blank=True, null=True)
    middle_name = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(default=timezone.now)

    # Profile Images
    profile_image = models.ImageField(upload_to='profile/', default='avatar.png', null=True, blank=True)
    image1 = models.ImageField(upload_to='profile/', null=True, blank=True, default='avatar.jpg')
    image2 = models.ImageField(upload_to='profile/', null=True, blank=True, default='avatar.jpg')
    image3 = models.ImageField(upload_to='profile/', null=True, blank=True, default='avatar.jpg')
    image4 = models.ImageField(upload_to='profile/', null=True, blank=True, default='avatar.jpg')
    image5 = models.ImageField(upload_to='profile/', null=True, blank=True, default='avatar.jpg')


    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username














# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# class User(AbstractUser):
#     MARITAL_STATUS_CHOICES = [
#         ('single', 'Single'),
#         ('married', 'Married'),
#         ('divorced', 'Divorced'),
#     ]
#     GENDER_CHOICES = [
#         ('male', 'male'),
#         ('female', 'female'),
#         ('other', 'other'),
#     ]
#     STATE_CHOICES = [
#         ('abia', 'Abia'),
#         ('abuja', 'Abuja'),
#         ('adamawa', 'Adamawa'),
#         ('akwa-ibom', 'Akwa-Ibom'),
#         ('anambra', 'Anambra'),
#         ('bauchi', 'Bauchi'),
#         ('bayelsa', 'Bayelsa'),
#         ('benue', 'Benue'),
#         ('borno', 'Borno'),
#         ('cross-Rivers', 'Cross-Rivers'),
#         ('delta', 'Delta'),
#         ('ebonyi', 'Ebonyi'),
#         ('edo', 'Edo'),
#         ('ekiti', 'Ekiti'),
#         ('enugu', 'Enugu'),
#         ('gombe', 'Gombe'),
#         ('imo', 'Imo'),
#         ('jigawa', 'Jigawa'),
#         ('kaduna', 'Kaduna'),
#         ('kano', 'Kano'),
#         ('katsina', 'Katsina'),
#         ('kebbi', 'Kebbi'),
#         ('kogi', 'Kogi'),
#         ('kwara', 'Kwara'),
#         ('lagos', 'Lagos'),
#         ('nasarawa', 'Nasarawa'),
#         ('niger', 'Niger'),
#         ('ogun', 'Ogun'),
#         ('ondo', 'Ondo'),
#         ('osun', 'Osun'),
#         ('oyo', 'Oyo'),
#         ('plateau', 'Plateau'),
#         ('rivers', 'Rivers'),
#         ('sokoto', 'Sokoto'),
#         ('taraba', 'Taraba'),
#         ('yobe', 'Yobe'),
#         ('zamfara', 'Zamfara'),
#     ]
#
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
#     looking_for = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
#     birthday = models.DateField(max_length=10, null=True)
#     state = models.CharField(max_length=15, choices=STATE_CHOICES, null=True)
#     marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='single')
#     bio = models.TextField(blank=True, null=True)
#     profile_image = models.ImageField(upload_to='profile/', default='avatar.jpg', null=True, blank=True)
#
#     def __str__(self):
#         return self.username
