from django.shortcuts import render
from accounts.models import User as AccountsUserProfile
from .models import UserProfile as FeedUserProfile

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User


def feed(request):
    # Query data from the accounts app's UserProfile model
    profiles = AccountsUserProfile.objects.all()
    print(f"Number of profiles fetched: {profiles.count()}")  # Debugging: Print count of profiles
    return render(request, 'feed/feed.html', {'profiles': profiles})

def prof(request):
    return render(request, "feed/prof.html")
