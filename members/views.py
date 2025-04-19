from django.shortcuts import render
from accounts.models import User as AccountsUserProfile
from .models import UserProfile as FeedUserProfile

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# @login_required
# def allmembers(request):
#     # Query data from the accounts app's UserProfile model
#     profiles = AccountsUserProfile.objects.all()
#     print(f"Number of profiles fetched: {profiles.count()}")  # Debugging: Print count of profiles
#     return render(request, 'members/members.html', {'profiles': profiles})

from django.core.paginator import Paginator

@login_required
def allmembers(request):
    profiles = AccountsUserProfile.objects.exclude(username=request.user.username)  # Exclude the current user
    paginator = Paginator(profiles, 20)  # Show 20 users per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'members/members.html', {'page_obj': page_obj})

def feed(request):
    # Query data from the accounts app's UserProfile model
    profiles = AccountsUserProfile.objects.all()
    print(f"Number of profiles fetched: {profiles.count()}")  # Debugging: Print count of profiles
    return render(request, 'members/feed.html', {'profiles': profiles})

def prof(request):
    return render(request, "members/prof.html")

def search_members(request):
    return render(request, "members/search_members.html")



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from members.models import UserProfile, Like
from accounts.models import User  # Use your custom user model if applicable

@login_required
def like_user(request, username):
    """
    Handle liking a user.
    """
    if request.method != 'POST':  # Ensure the request is POST
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return JsonResponse({'status': 'error', 'message': "You can't like yourself."}, status=400)

    like, created = Like.objects.get_or_create(user_from=request.user, user_to=other_user)

    if created:
        if Like.objects.filter(user_from=other_user, user_to=request.user).exists():
            return JsonResponse({'status': 'match', 'message': f"You matched with {other_user.username}!"}, status=200)
        return JsonResponse({'status': 'liked', 'message': f"You liked {other_user.username}!"}, status=200)

    return JsonResponse({'status': 'already_liked', 'message': f"You already liked {other_user.username}!"}, status=200)



@login_required
def matched_users(request):
    user = request.user
    matched_users = User.objects.filter(
        likes_received__user_from=user,
        likes_sent__user_to=user
    )
    return render(request, "members/cht.html", {"matched_users": matched_users})
