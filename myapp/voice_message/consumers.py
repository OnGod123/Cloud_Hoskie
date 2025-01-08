import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from myapp.models import Person


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.recipient_username = self.scope['url_route']['kwargs']['recipientUsername']
        self.room_group_name = f"chat_{self.username}_{self.recipient_username}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == 'text':
                message = text_data_json.get('data')
                sender = self.scope['user']
                recipient = User.objects.get(username=self.recipient_username)

                # Save message to database
                Message.objects.create(
                    sender=sender,
                    recipient=recipient,
                    content=message
                )
   # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender': sender.username
                    }
                )

            elif message_type == 'offer' or message_type == 'answer' or message_type == 'candidate':
                # Forward WebRTC signaling messages
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'signaling_message',
                        'data': text_data_json
                    }
                )
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'text',
            'message': event['message'],
            'sender': event['sender']
        }))

    async def signaling_message(self, event):
        # Forward WebRTC signaling message to WebSocket
        await self.send(text_data=json.dumps(event['data']))
