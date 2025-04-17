import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Community, Person, LiveSession

class LiveSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract community ID from the URL and validate user membership
        self.community_id = self.scope['url_route']['kwargs']['community_id']
        self.group_name = f"community_{self.community_id}"

        # Check if the user is part of the community
        user = self.scope["user"]
        is_member = await self.check_membership(user, self.community_id)

        if is_member:
            # Add the WebSocket connection to the group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            # Reject connection if the user is not a member
            await self.close()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Broadcast the received data to all members in the group
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('message_type', 'text')
        message_content = text_data_json.get('content', '')

        # Forward the message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'live_session_message',
                'message_type': message_type,
                'content': message_content,
            }
        )

    async def live_session_message(self, event):
        # Send the message to the WebSocket of every connected member
        await self.send(text_data=json.dumps({
            'message_type': event['message_type'],
            'content': event['content'],
        }))

    @sync_to_async
    def check_membership(self, user, community_id):
        # Check if the user is a member of the given community
        return Community.objects.filter(id=community_id, members=user).exists()