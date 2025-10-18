import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

# ❌ Remove the top-level call

class ChatConsumer(AsyncWebsocketConsumer):
    @staticmethod
    async def get_user(username):
        User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        from .models import Message
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id
        receiver_username = data['receiver']

        receiver = await self.get_user(receiver_username)

        # ✅ Save message
        await self.save_message(sender_id, receiver.id, message, self.room_name)

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        from .models import Message
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @staticmethod
    async def get_user(username):
        from .models import Message
        from django.contrib.auth import get_user_model   # ✅ Import here instead
        User = get_user_model()
        return await User.objects.aget(username=username)

    @staticmethod
    async def save_message(sender_id, receiver_id, message, room_name):
        from .models import Message
        await Message.objects.acreate(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=message,
            room_name=room_name
        )
