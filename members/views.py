from django.shortcuts import render
from accounts.models import User as AccountsUserProfile
from .models import UserProfile as FeedUserProfile

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# @login_required
# def allmembers(request):
#     # Query data from the accounts app's UserProfile model
#     profiles = AccountsUserProfile.objects.all()
#     print(f"Number of profiles fetched: {profiles.count()}")  # Debugging: Print count of profiles
#     return render(request, 'members/members.html', {'profiles': profiles})

from django.core.paginator import Paginator

@login_required
def allmembers(request):
    profiles = AccountsUserProfile.objects.exclude(username=request.user.username)

    # ✅ Get the IDs of users the current user has already liked
    liked_user_ids = Like.objects.filter(user_from=request.user).values_list('user_to__id', flat=True)

    paginator = Paginator(profiles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'members/members.html', {
        'page_obj': page_obj,
        'liked_user_ids': liked_user_ids
    })

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

@never_cache
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


# from django.utils import timezone
# @login_required
# def matched_users(request):
#     request.user.last_checked_messages_at = timezone.now()
#     request.user.save(update_fields=['last_checked_messages_at'])
#
#     user = request.user
#     matched_users = User.objects.filter(
#         likes_received__user_from=user,
#         likes_sent__user_to=user
#     )
#     return render(request, "members/cht.html", {"matched_users": matched_users})


from datetime import datetime, timezone as dt_timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from chat.models import ChatRoom, ChatMessage
from accounts.models import User  # Your custom User model

@never_cache
@login_required
def matched_users(request):
    request.user.last_checked_messages_at = timezone.now()
    request.user.save(update_fields=['last_checked_messages_at'])

    user = request.user
    # Get users that match with current user
    matched_users = User.objects.filter(
        likes_received__user_from=user,
        likes_sent__user_to=user
    ).distinct()

    matched_users_with_last_msg = []
    for matched in matched_users:
        # Get the chat room between both users
        room = ChatRoom.objects.filter(
            (Q(user1=user) & Q(user2=matched)) | (Q(user1=matched) & Q(user2=user))
        ).first()

        last_msg = (
            ChatMessage.objects
            .filter(room=room)
            .order_by('-timestamp')
            .first()
        )

        matched_users_with_last_msg.append({
            'user': matched,
            'last_msg_time': last_msg.timestamp if last_msg else None,
            'last_msg_text': last_msg.message if last_msg else None,
            'last_msg_read': True if not last_msg else (last_msg.is_read or last_msg.sender == request.user)
        })

    # Sort by last message time (most recent first)
    matched_users_with_last_msg.sort(
        key=lambda x: x['last_msg_time'] or datetime.min.replace(tzinfo=dt_timezone.utc),
        reverse=True
    )

    return render(request, "members/cht.html", {
        "matched_users": matched_users_with_last_msg
    })





from django.shortcuts import render, get_object_or_404
from accounts.models import User  # or your custom user model

@never_cache
@login_required
def user_profile(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    return render(request, 'members/user_profile.html', {'profile': user_profile})
