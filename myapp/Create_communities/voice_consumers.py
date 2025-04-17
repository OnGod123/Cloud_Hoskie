import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CommunityVoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get community ID from the WebSocket URL
        self.community_id = self.scope['url_route']['kwargs']['community_id']
        self.group_name = f"community_{self.community_id}"

        # Add socket to group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove this socket from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming WebSocket message
        text_data_json = json.loads(text_data)
        sender = text_data_json['sender']
        content = text_data_json.get('content', '')  # Optional
        message_type = text_data_json.get('message_type', 'text')
        voice_file_url = text_data_json.get('voice_file_url', '')

        # Broadcast to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_message',
                'sender': sender,
                'content': content,
                'message_type': message_type,
                'voice_file_url': voice_file_url,
            }
        )

    async def broadcast_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'content': event['content'],
            'message_type': event['message_type'],
            'voice_file_url': event['voice_file_url'],
        }))