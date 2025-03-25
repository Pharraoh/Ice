from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatMessage
from accounts.models import User  # Replace with your custom user model if applicable
from django.http import JsonResponse
from django.db.models import Max
from django.core.cache import cache

@login_required
def one_on_one_chat(request, username):
    """
    View to handle one-on-one chat between two users.
    """

    other_user = get_object_or_404(User, username=username)


    user1, user2 = sorted([request.user, other_user], key=lambda x: x.id)

    room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2)

    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:

            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message=message_content
            )
            return redirect('chats:one_on_one_chat', username=username)

    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')


    rooms = ChatRoom.objects.filter(user1=request.user) | ChatRoom.objects.filter(user2=request.user)
    chat_partners = []
    for r in rooms:
        if r.user1 == request.user:
            chat_partners.append(r.user2)
        else:
            chat_partners.append(r.user1)

    return render(request, 'chat/one_on_one_chat.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user,
        'chat_partners': chat_partners,
    })



# from django.db import models
# from django.contrib.auth import get_user_model
# from django.shortcuts import render, get_object_or_404
# from .models import ChatMessage, ChatRoom
#
# User = get_user_model()
#
# def one_on_one_chat(request, username):
#     other_user = get_object_or_404(User, username=username)
#
#
#     chat_room = ChatRoom.objects.filter(
#         (models.Q(user1=request.user) & models.Q(user2=other_user)) |
#         (models.Q(user1=other_user) & models.Q(user2=request.user))
#     ).first()
#
#     messages = ChatMessage.objects.filter(room=chat_room).order_by('timestamp') if chat_room else []
#
#     return render(request, 'chat/one_on_one_chat.html', {
#         'other_user': other_user,
#         'messages': messages,
#     })




# from django.template.loader import render_to_string
# from django.http import JsonResponse
#
# @login_required
# def one_on_one_chat(request, username):
#     other_user = get_object_or_404(User, username=username)
#     user1, user2 = sorted([request.user, other_user], key=lambda x: x.id)
#     room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2)
#     messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
#
#
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string('chat/partials/one_on_one_chat.html', {
#             'messages': messages,
#             'other_user': other_user,
#         })
#         return JsonResponse({'html': html})
#
#
#     chat_partners = [...]
#     return render(request, 'chat/one_on_one_chat.html', {
#         'messages': messages,
#         'other_user': other_user,
#         'chat_partners': chat_partners,
#     })



@login_required
def chat_list(request):
    """
    View to display a list of users the current user has chatted with.
    """

    rooms = ChatRoom.objects.filter(user1=request.user) | ChatRoom.objects.filter(user2=request.user)


    chat_partners = []
    for room in rooms:
        if room.user1 == request.user:
            chat_partners.append(room.user2)
        else:
            chat_partners.append(room.user1)

    return render(request, 'chat/cht.html', {
        'chat_partners': chat_partners,
    })





from django.http import JsonResponse
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import logging
from .models import ChatRoom, ChatMessage
from accounts.models import User

logger = logging.getLogger(__name__)

@login_required
def fetch_messages(request, username):
    logger.info(f"🔍 Fetching messages for {request.user} and {username}")

    try:
        # ✅ Print received username for debugging
        print(f"🔍 Received username for fetching messages: {username}")

        # ✅ Ensure other user exists
        other_user = get_object_or_404(User, username=username)

        # ✅ Find chat room
        room = ChatRoom.objects.filter(
            models.Q(user1=request.user, user2=other_user) |
            models.Q(user1=other_user, user2=request.user)
        ).first()

        if not room:
            logger.warning(f"⚠️ No chat room found between {request.user} and {username}")
            return JsonResponse({'messages': []})

        # ✅ Fetch messages (ordering ensures newest at the bottom)
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')

        # ✅ Log messages
        print(f"💬 DEBUG: Found {messages.count()} messages for chat {room.id}")
        for msg in messages:
            print(f"📝 {msg.sender.username}: {msg.message} ({msg.timestamp})")

        # ✅ Format messages for JSON response
        messages_data = [
            {
                'sender': message.sender.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for message in messages
        ]

        return JsonResponse({'messages': messages_data})

    except Exception as e:
        logger.error(f"❌ ERROR in fetch_messages: {str(e)}")
        return JsonResponse({'error': 'Something went wrong'}, status=500)












#
# @login_required
# def fetch_messages(request, room_id):
#     """
#     AJAX endpoint to fetch messages for a specific chat room.
#     """
#     room = get_object_or_404(ChatRoom, id=room_id)
#
#     if request.user not in [room.user1, room.user2]:
#         return JsonResponse({'error': 'Unauthorized'}, status=403)
#
#     messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
#
#     messages_data = [
#         {
#             'sender': message.sender.username,
#             'message': message.message,
#             'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#         }
#         for message in messages
#     ]
#
#     return JsonResponse({'messages': messages_data})



# @login_required
# def send_message(request, room_id):
#     room = get_object_or_404(ChatRoom, id=room_id)
#
#     if request.method == "POST":
#         data = json.loads(request.body)
#         message = data.get("message")
#         if message:
#             ChatMessage.objects.create(
#                 room=room,
#                 sender=request.user,
#                 message=message
#             )
#             return JsonResponse({"status": "success"})
#     return JsonResponse({"status": "error", "message": "Invalid request"})





from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import ChatRoom, ChatMessage
from accounts.models import User
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

@login_required
def send_message(request, username):
    """Handles sending messages and saving them in the database."""
    logger.info(f"🚀 DEBUG: Received send_message request from {request.user} to {username}")

    try:
        other_user = get_object_or_404(User, username=username)
        logger.info(f"✅ DEBUG: Found recipient {other_user}")

        # ✅ Ensure the correct chat room is used
        user1, user2 = sorted([request.user, other_user], key=lambda x: x.id)
        room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2)

        if request.method == "POST":
            logger.info(f"📩 DEBUG: Processing POST request for room {room.id}")

            data = json.loads(request.body)
            message_text = data.get("message")

            if not message_text:
                logger.warning("⚠️ DEBUG: Empty message!")
                return JsonResponse({"status": "error", "message": "Message cannot be empty"}, status=400)

            # ✅ Force database transaction commit
            with transaction.atomic():
                new_message = ChatMessage.objects.create(
                    room=room,
                    sender=request.user,
                    message=message_text
                )
                logger.info(f"💾 DEBUG: Message saved! {new_message.message}")

            # ✅ Force Django to refresh and commit DB changes
            from django.db import connection
            connection.close()

            return JsonResponse({
                "status": "success",
                "message": new_message.message,
                "sender": new_message.sender.username,
                "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            })

    except Exception as e:
        logger.error(f"❌ DEBUG: Error in send_message: {str(e)}")
        return JsonResponse({"status": "error", "message": "Something went wrong"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)






from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Status
from accounts.models import User
import json

from django.core.files.storage import default_storage

@login_required
def post_status(request):
    """Handles posting a new status (text, image, or video)."""
    if request.method == "POST":
        user = request.user
        data = request.POST

        status_type = data.get("status_type")
        text = data.get("text", "").strip()
        media = request.FILES.get("media", None)  # Image or video file

        print(f"📝 DEBUG: Received status request - {status_type}")

        if status_type not in ["text", "image", "video"]:
            print("❌ Invalid status type")
            return JsonResponse({"status": "error", "message": "Invalid status type."}, status=400)

        if status_type == "text" and not text:
            print("❌ Text status cannot be empty")
            return JsonResponse({"status": "error", "message": "Text status cannot be empty."}, status=400)

        # Save the status
        status = Status.objects.create(user=user, status_type=status_type, text=text, media=media)
        print(f"✅ Status saved: {status}")

        return JsonResponse({"status": "success", "message": "Status posted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)





from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Status
from accounts.models import User

@login_required
def fetch_statuses(request):
    user = request.user

    # ✅ Get matched users + the logged-in user
    matched_users = User.objects.filter(
        likes_received__user_from=user,
        likes_sent__user_to=user
    ) | User.objects.filter(id=user.id)  # Include self

    expiry_time = now() - timedelta(hours=24)  # ✅ Fetch only the last 24 hours' statuses
    statuses = Status.objects.filter(user__in=matched_users, created_at__gte=expiry_time).order_by("-created_at")

    # ✅ Format response (include time remaining)
    status_data = [
        {
            "username": status.user.username,
            "profile_image": status.user.profile_image.url if status.user.profile_image else "/static/default.jpg",
            "status_type": status.status_type,
            "text": status.text if status.text else "",
            "media_url": status.media.url if status.media else "",
            "timestamp": status.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_in": (status.created_at + timedelta(hours=24)).isoformat(),  # ✅ Expiration timestamp
            "is_owner": status.user == user,
        }
        for status in statuses
    ]

    return JsonResponse({"statuses": status_data})
