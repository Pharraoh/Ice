from chat.models import ChatMessage
from django.db.models import Q


def new_message_flag(request):
    if request.user.is_authenticated:
        has_new = ChatMessage.objects.filter(
            room__user1=request.user
        ).exclude(sender=request.user).exists() or ChatMessage.objects.filter(
            room__user2=request.user
        ).exclude(sender=request.user).exists()
    return {}
