from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message
from .utils import get_room_name

User = get_user_model()


from accounts.models import User
from realtime_chat.models import Message
from realtime_chat.utils import get_room_name  # assuming you have this helper


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)

    # ✅ Check if current user and other_user are matched
    is_matched = User.objects.filter(
        Q(id=request.user.id),
        Q(likes_sent__user_to=other_user),
        Q(likes_received__user_from=other_user)
    ).exists()

    if not is_matched:
        return redirect('realtime_chat:matched_users')

    # ✅ Room name logic
    room_name = get_room_name(request.user, other_user)
    messages = Message.objects.filter(room_name=room_name).select_related('sender', 'receiver')

    # ✅ Fetch all *mutual* matches for sidebar
    matched_users = User.objects.filter(
        likes_received__user_from=request.user,
        likes_sent__user_to=request.user
    ).distinct()

    context = {
        'room_name': room_name,
        'other_user': other_user,
        'messages': messages,
        'matched_users': matched_users,
    }

    return render(request, 'realtime_chat/chat_room.html', context)



from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def mark_chat_read(request, username):
    other_user = get_object_or_404(User, username=username)
    room_name = get_room_name(request.user, other_user)

    # Mark messages as read
    unread_qs = Message.objects.filter(
        receiver=request.user,
        sender=other_user,
        is_read=False
    )

    if unread_qs.exists():
        count = unread_qs.count()
        unread_qs.update(is_read=True)
        print(f"[DEBUG] Marked {count} messages as read")

        # Send WebSocket update
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()

        async_to_sync(channel_layer.group_send)(
            f"user_{request.user.id}",
            {
                "type": "notify_unread",
                "unread_count": unread_count,
            }
        )

        return JsonResponse({'success': True, 'unread_count': unread_count})

    return JsonResponse({'success': True, 'unread_count': 0})



from .models import Message

@login_required
def unread_count_view(request):
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})



# @login_required
# def chat_view(request, username):
#     other_user = get_object_or_404(User, username=username)
#
#     # ✅ Check if current user and other_user are matched
#     is_matched = User.objects.filter(
#         Q(id=request.user.id),
#         Q(likes_sent__user_to=other_user),
#         Q(likes_received__user_from=other_user)
#     ).exists()
#
#     if not is_matched:
#         return redirect('realtime_chat:matched_users')
#
#     # ✅ Room name logic
#     room_name = get_room_name(request.user, other_user)
#     messages = Message.objects.filter(room_name=room_name).select_related('sender', 'receiver')
#
#     # ✅ Fetch all *mutual* matches for sidebar
#     matched_users = User.objects.filter(
#         likes_received__user_from=request.user,
#         likes_sent__user_to=request.user
#     ).distinct()
#
#     context = {
#         'room_name': room_name,
#         'other_user': other_user,
#         'messages': messages,
#         'matched_users': matched_users,
#     }
#
#     return render(request, 'realtime_chat/chat_room.html', context)



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from accounts.models import User

# @login_required
# def matched_users_view(request):
#     user = request.user
#
#     # ✅ Get only users who have mutual likes with the current user
#     matched_users = User.objects.filter(
#         likes_received__user_from=user,
#         likes_sent__user_to=user
#     ).distinct()
#
#     return render(request, 'realtime_chat/matched_users.html', {
#         'matched_users': matched_users
#     })


# @login_required
# def matched_users_view(request):
#     matched_users = User.objects.filter(
#         likes_received__user_from=request.user,
#         likes_sent__user_to=request.user
#     ).distinct()
#
#     return render(request, 'realtime_chat/matched_users.html', {'matched_users': matched_users})


from django.db.models import Q
from realtime_chat.models import Message  # adjust import if needed

from realtime_chat.models import Message
from accounts.models import User

from django.utils import timezone
from datetime import timedelta

@login_required
def matched_users_view(request):
    matched_users = User.objects.filter(
        likes_received__user_from=request.user,
        likes_sent__user_to=request.user
    ).distinct()

    matched_data = []

    for user in matched_users:
        last_msg = Message.objects.filter(
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()

        # ✅ Format human-friendly time
        if last_msg:
            now = timezone.now()
            diff = now - last_msg.timestamp

            if diff.days == 0:
                # Same day → show exact time like "2:45 PM"
                time_display = last_msg.timestamp.strftime("%I:%M %p")
            elif diff.days == 1:
                time_display = "Yesterday"
            else:
                # Older → show date like "Oct 10"
                time_display = last_msg.timestamp.strftime("%b ") + str(last_msg.timestamp.day)
        else:
            time_display = None

        matched_data.append({
            'user': user,
            'last_message': last_msg.content if last_msg else None,
            'last_message_sender': last_msg.sender.username if last_msg else None,
            'timestamp': time_display,  # 👈 formatted string
            'is_read': last_msg.is_read if last_msg else True,
        })

    return render(request, 'realtime_chat/matched_users.html', {'matched_data': matched_data})









# status implementation
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Status
from accounts.models import User
import json

from django.core.files.storage import default_storage

from django.utils.timezone import now
from .models import Status
import tempfile, os
os.environ["SDL_AUDIODRIVER"] = "dummy"
from moviepy.editor import VideoFileClip



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Status
from moviepy.editor import VideoFileClip
import tempfile

@login_required
def post_status(request):
    if request.method == "POST":
        user = request.user
        data = request.POST
        media = request.FILES.get("media")
        status_type = data.get("status_type")
        text = data.get("text", "").strip()
        caption = data.get("caption", "").strip()

        # Validate status_type
        if status_type not in ["text", "image", "video"]:
            return JsonResponse({"status": "error", "message": "Invalid status type."}, status=400)

        # Validate text content
        if status_type == "text" and not text:
            return JsonResponse({"status": "error", "message": "Text status cannot be empty."}, status=400)

        # Validate caption length
        if len(caption) > 100:
            return JsonResponse({"status": "error", "message": "Caption too long. Max 100 characters."}, status=400)

        # File validations
        if media:
            MAX_FILE_SIZE_MB = 20
            if media.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                return JsonResponse({
                    "status": "error",
                    "message": f"File too large. Max allowed is {MAX_FILE_SIZE_MB}MB."
                }, status=400)

        # Optional: Validate video duration
        if status_type == "video" and media:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                    for chunk in media.chunks():
                        temp_file.write(chunk)
                    temp_file.flush()
                    clip = VideoFileClip(temp_file.name)
                    duration = clip.duration
                if duration > 30:
                    return JsonResponse({"status": "error", "message": "Video too long. Max 30 seconds."}, status=400)
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Could not process video: {str(e)}"}, status=400)

        # Save to DB
        status_kwargs = {
            "user": user,
            "status_type": status_type,
            "caption": caption,
        }

        if status_type == "video":
            status_kwargs["video"] = media
        elif status_type == "image":
            status_kwargs["image"] = media
        elif status_type == "text":
            status_kwargs["text"] = text

        Status.objects.create(**status_kwargs)

        return JsonResponse({"status": "success", "message": "Status posted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)







from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Status
from accounts.models import User

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from .models import Status, User  # adjust User import as needed

@login_required
def fetch_statuses(request):
    user = request.user

    # ✅ Get matched users + the logged-in user
    matched_users = User.objects.filter(
        likes_received__user_from=user,
        likes_sent__user_to=user
    ) | User.objects.filter(id=user.id)  # Include self

    expiry_time = now() - timedelta(hours=24)
    statuses = Status.objects.filter(
        user__in=matched_users,
        created_at__gte=expiry_time
    ).order_by("-created_at")

    status_data = [
        {
            "username": status.user.username,
            "profile_image": status.user.profile_image.url if status.user.profile_image else "/static/default.jpg",
            "status_type": status.status_type,
            "text": status.text or "",
            "media_url": (
                status.image.url if status.status_type == "image" and status.image else
                status.video.url if status.status_type == "video" and status.video else
                ""
            ),
            "timestamp": status.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_in": (status.created_at + timedelta(hours=24)).isoformat(),
            "is_owner": status.user == request.user,
            "id": str(status.id),
            "caption": status.caption or "",
        }
        for status in statuses
    ]

    return JsonResponse({"statuses": status_data})



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Status

@login_required
def delete_status(request, status_id):
    if request.method == "POST":
        status = get_object_or_404(Status, id=status_id, user=request.user)
        status.delete()
        return JsonResponse({"status": "success", "message": "Status deleted successfully!"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
