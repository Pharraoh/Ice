from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth.models import User

from django.db import models
from django.conf import settings



class User(AbstractUser):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_creator = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_pics/', default='1.png', null=True, blank=True)
    phone_no = models.CharField(max_length=11, default=00000)
    bio = models.TextField(max_length=500, blank=True)
    LOCATION_CHOICES = [
        ('Ado', 'Ado'),
        ('Campus', 'Campus'),
        ('Iworoko', 'Iworoko'),
        ('Main Gate', 'Main Gate'),
        ('Osekita', 'Osekita'),
        ('Phase II', 'Phase II'),
        ('Satellite', 'Satellite'),
        ('UBA', 'UBA'),
        ('Unity', 'Unity')
    ]
    location = models.CharField(default='nil', max_length=30, choices=LOCATION_CHOICES)
    company = models.CharField(max_length=20, null=True, blank=True)
    CATEGORY_CHOICES = [
        ('Affiliate Marketing', 'Affiliate Marketing'),
        ('Arts & Entertainment', 'Arts & Entertainment'),
        ('Clothing', 'Clothing'),
        ('Education & Tutoring', 'Education & Tutoring'),
        ('Food & Restaurants', 'Food & Restaurants'),
        ('Hostels & Accomodations', 'Hostels & Accomodations'),
        ('Music', 'Music'),
        ('Sports & Excercise', 'Sports & Excercise'),
        ('Tech', 'Tech'),
    ]
    category = models.CharField(default='nil', max_length=50, choices=CATEGORY_CHOICES)
    facebook_link = models.CharField(default='nil', max_length=500)
    whatsapp_link = models.CharField(default='nil', max_length=500)
    instagram_link = models.CharField(default='nil', max_length=500)
    tiktok_link = models.CharField(default='nil', max_length=500)
    website_link = models.CharField(default='nil', max_length=500)
    # birth_date = models.DateTimeField(max_length=3, null=True, blank=True)
    # state = models.CharField(max_length=10)
    # country = models.CharField(max_length=10)


    def get_absolute_url(self):
        return reverse('accounts:dashboard')

class Post(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    LOCATION_CHOICES = [
        ('Ado', 'Ado'),
        ('Campus', 'Campus'),
        ('Iworoko', 'Iworoko'),
        ('Main Gate', 'Main Gate'),
        ('Osekita', 'Osekita'),
        ('Phase II', 'Phase II'),
        ('Satellite', 'Satellite'),
        ('UBA', 'UBA'),
        ('Unity', 'Unity')
    ]
    location = models.CharField(default='nil', max_length=30, choices=LOCATION_CHOICES)
    CATEGORY_CHOICES = [
        ('Affiliate Marketing', 'Affiliate Marketing'),
        ('Arts & Entertainment', 'Arts & Entertainment'),
        ('Clothing', 'Clothing'),
        ('Education & Tutoring', 'Education & Tutoring'),
        ('Food & Restaurants', 'Food & Restaurants'),
        ('Hostels & Accomodations', 'Hostels & Accomodations'),
        ('Music', 'Music'),
        ('Sports & Excercise', 'Sports & Excercise'),
        ('Tech', 'Tech'),
    ]
    category = models.CharField(default='nil', max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField(max_length=400)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')


    def __str__(self):
        return self.title
