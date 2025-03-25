from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatMessage
from accounts.models import User  # Replace with your custom user model if applicable
from django.http import JsonResponse
from django.db.models import Max

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

    return render(request, 'chat/chat3.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user,
        'chat_partners': chat_partners,
    })


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

    return render(request, 'chat/chat_list_demo.html', {
        'chat_partners': chat_partners,
    })






@login_required
def fetch_messages(request, room_id):
    """
    AJAX endpoint to fetch messages for a specific chat room.
    """
    room = get_object_or_404(ChatRoom, id=room_id)

    # Ensure the current user belongs to this room
    if request.user not in [room.user1, room.user2]:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Get messages for this room
    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')

    # Serialize messages for the response
    messages_data = [
        {
            'sender': message.sender.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for message in messages
    ]

    return JsonResponse({'messages': messages_data})



@login_required
def send_message(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        if message:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message=message
            )
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
