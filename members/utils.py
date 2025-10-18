# members/utils.py
from django.db.models import Q
from accounts.models import User

def get_matched_users(user):
    """
    Returns a queryset of users who have mutually liked the given user.
    """
    matched_users = User.objects.filter(
        likes_received__user_from=user,
        likes_sent__user_to=user
    ).distinct()
    return matched_users
