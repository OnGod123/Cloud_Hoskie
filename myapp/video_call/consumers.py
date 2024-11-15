import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from myapp.video_call.models import VideoCall
from myapp.models import  Person

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract usernames from the URL route
        self.initiator_username = self.scope['url_route']['kwargs']['initiator']
        self.recipient_username = self.scope['url_route']['kwargs']['recipient']
        self.room_group_name = f'webrtc_{self.initiator_username}_{self.recipient_username}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # Create a new VideoCall instance when a call is initiated
        try:
            initiator = Person.objects.get(username=self.initiator_username)
            recipient = Person.objects.get(username=self.recipient_username)

            # Create a new call instance
            VideoCall.objects.create(
                initiator=initiator,
                recipient=recipient,
                start_time=timezone.now(),
                status='active'
            )
        except Person.DoesNotExist:
            await self.close(code=4001)  # Close with custom error code if user is not found

    async def disconnect(self, close_code):
        # Update the VideoCall status to 'ended' when the WebSocket disconnects
        try:
            VideoCall.objects.filter(
                initiator__username=self.initiator_username,
                recipient__username=self.recipient_username,
                status='active'
            ).update(end_time=timezone.now(), status='ended')
        except VideoCall.DoesNotExist:
            pass  # Handle any edge cases where the call record is not found

        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        data = text_data_json['data']

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'webrtc_message',
                'message_type': message_type,
                'data': data
            }
        )

    async def webrtc_message(self, event):
        message_type = event['message_type']
        data = event['data']

        # Send the message to the WebSocket client
        await self.send(text_data=json.dumps({
            message_type: data
        }))
