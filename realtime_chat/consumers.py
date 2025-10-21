# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth import get_user_model
#
# # ❌ Remove the top-level call
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     @staticmethod
#     async def get_user(username):
#         User = get_user_model()
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f"chat_{self.room_name}"
#
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#
#     async def receive(self, text_data):
#         from .models import Message
#         data = json.loads(text_data)
#         message = data['message']
#         sender_id = self.scope['user'].id
#         receiver_username = data['receiver']
#
#         receiver = await self.get_user(receiver_username)
#
#         # ✅ Save message
#         await self.save_message(sender_id, receiver.id, message, self.room_name)
#
#         # Broadcast message to group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': self.scope['user'].username,
#             }
#         )
#
#     async def chat_message(self, event):
#         from .models import Message
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender']
#         }))
#
#     @staticmethod
#     async def get_user(username):
#         from .models import Message
#         from django.contrib.auth import get_user_model   # ✅ Import here instead
#         User = get_user_model()
#         return await User.objects.aget(username=username)
#
#     @staticmethod
#     async def save_message(sender_id, receiver_id, message, room_name):
#         from .models import Message
#         await Message.objects.acreate(
#             sender_id=sender_id,
#             receiver_id=receiver_id,
#             content=message,
#             room_name=room_name
#         )




import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    @staticmethod
    async def get_user(username):
        User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    from .models import Message
    async def connect(self):
        # Main chat room group (for messages)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Personal notification group (for unread badge updates)
        self.user_group_name = f"user_{self.scope['user'].id}"

        # Join both groups
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def receive(self, text_data):
        from .models import Message
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']
        receiver_username = data['receiver']

        receiver = await self.get_user(receiver_username)

        # ✅ Save message
        await self.save_message(sender.id, receiver.id, message, self.room_name)

        # Broadcast the chat message to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
            }
        )

        # ✅ Notify receiver’s personal group with updated unread count
        unread_count = await self.get_unread_count(receiver)
        await self.channel_layer.group_send(
            f"user_{receiver.id}",
            {
                'type': 'notify_unread',
                'unread_count': unread_count,
            }
        )

    async def chat_message(self, event):
        from .models import Message
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
        }))

    async def notify_unread(self, event):
        from .models import Message
        """Send unread count update to the receiver."""
        await self.send(text_data=json.dumps({
            'type': 'notify_unread',
            'unread_count': event['unread_count'],
        }))

    @database_sync_to_async
    def get_user(self, username):
        from .models import Message
        from django.contrib.auth import get_user_model   # ✅ Import here instead
        User = get_user_model()
        return User.objects.get(username=username)

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message, room_name):
        from .models import Message
        return Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=message,
            room_name=room_name
        )

    @database_sync_to_async
    def get_unread_count(self, user):
        from .models import Message
        return Message.objects.filter(receiver=user, is_read=False).count()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
        else:
            self.user_group_name = f"user_{user.id}"
            await self.channel_layer.group_add(self.user_group_name, self.channel_name)
            await self.accept()

            # Optionally send current unread count immediately
            unread_count = await self.get_unread_count(user)
            print(f"[DEBUG] Connected user: {user}, unread_count={unread_count}")  # 👈 Add this

            await self.send(text_data=json.dumps({
                'type': 'notify_unread',
                'unread_count': unread_count,
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def notify_unread(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notify_unread',
            'unread_count': event['unread_count'],
        }))

    @database_sync_to_async
    def get_unread_count(self, user):
        from .models import Message
        return Message.objects.filter(receiver=user, is_read=False).count()
