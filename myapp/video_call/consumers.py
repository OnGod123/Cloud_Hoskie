import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from myapp.video_call.models import VideoCall
from myapp.models import Person
from asgiref.sync import sync_to_async


class SimpleWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Send a simple message to the client
        await self.send(text_data=json.dumps({
            'message': 'Connection successful!'
        }))

    async def disconnect(self, close_code):
        # This will be called when the WebSocket closes
        print(f'Connection closed with code {close_code}')

    async def receive(self, text_data):
        # This will handle any message sent from the client
        pass



class SimpleWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Send a simple message to the client
        await self.send(text_data=json.dumps({
            'message': 'Connection successful!'
        }))

    async def disconnect(self, close_code):
        # This will be called when the WebSocket closes
        print(f'Connection closed with code {close_code}')

    async def receive(self, text_data):
        # This will handle any message sent from the client
        pass

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
            initiator = await sync_to_async(Person.objects.get)(username=self.initiator_username)
            recipient = await sync_to_async(Person.objects.get)(username=self.recipient_username)

            # Create a new call instance
            await sync_to_async(VideoCall.objects.create)(
                initiator=initiator,
                recipient=recipient,
                start_time=timezone.now(),
                status='active'
            )
        except Person.DoesNotExist:
            await self.close(code=4001)  # Close with custom error code if user is not found

        # Start periodic pinging
        self.ping_task = asyncio.create_task(self.send_ping())

    async def disconnect(self, close_code):
        # Update the VideoCall status to 'ended' when the WebSocket disconnects
        try:
            # Ensure the update is awaited since sync_to_async returns a coroutine
            await sync_to_async(VideoCall.objects.filter)(
                initiator__username=self.initiator_username,
                recipient__username=self.recipient_username,
                status='active'
            ).update(end_time=timezone.now(), status='ended')
        except VideoCall.DoesNotExist:
            pass  # Handle any edge cases where the call record is not found

        # Cancel the ping task when disconnecting
        if hasattr(self, 'ping_task'):
            self.ping_task.cancel()

        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        data = text_data_json['data']

        # If the message type is 'ping', respond with a pong
        if message_type == 'ping':
            await self.send(text_data=json.dumps({
                'type': 'pong',
                'data': data  # Echo back the ping data if needed
            }))
        else:
            # Broadcast the message to the room group (for non-ping messages)
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

    async def send_ping(self):
        while True:
            try:
                # Ensure we're not sending messages after the connection has been closed
                if self.channel_name in self.application_channel_names:
                    await self.send(text_data=json.dumps({
                        'type': 'ping',
                        'data': 'ping'  # Customize this payload if needed
                    }))
                await asyncio.sleep(10)  # Ping every 10 seconds
            except (Disconnected, RuntimeError):
                # Handle the case when WebSocket is closed or some other runtime error
                break
