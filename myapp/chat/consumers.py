import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now
from asgiref.sync import sync_to_async
from myapp.models import ChatSession, ChatMessage, TypingIndicator


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract usernames from the URL route
        self.initiator_username = self.scope['url_route']['kwargs']['initiator']
        self.recipient_username = self.scope['url_route']['kwargs']['recipient']
        self.room_group_name = f"chat_{self.initiator_username}_{self.recipient_username}"

        # Add this connection to the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept WebSocket connection
        await self.accept()

        # Ensure a ChatSession exists
        self.chat_session = await self.get_or_create_chat_session()

    async def disconnect(self, close_code):
        # Remove this connection from the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # End the session if necessary
        await self.end_chat_session()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")
        content = text_data_json.get("content")

        # Handle chat messages
        if message_type == "chat_message":
            await self.save_message(content)

            # Broadcast the message to the recipient
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "sender": self.initiator_username,
                    "content": content,
                },
            )

        # Handle typing indicators
        elif message_type == "typing":
            is_typing = text_data_json.get("is_typing", False)
            await self.update_typing_indicator(is_typing)

            # Notify the recipient
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_indicator",
                    "user": self.initiator_username,
                    "is_typing": is_typing,
                },
            )

    async def chat_message(self, event):
        # Send the chat message to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "sender": event["sender"],
            "content": event["content"],
        }))

    async def typing_indicator(self, event):
        # Send the typing indicator to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user": event["user"],
            "is_typing": event["is_typing"],
        }))

    @sync_to_async
    def get_or_create_chat_session(self):
        # Ensure a ChatSession exists between the two users
        initiator = User.objects.get(username=self.initiator_username)
        recipient = User.objects.get(username=self.recipient_username)

        session, _ = ChatSession.objects.get_or_create(
            initiator=initiator,
            recipient=recipient,
            active=True,
        )
        return session

    @sync_to_async
    def save_message(self, content):
        # Save the message in the database
        sender = User.objects.get(username=self.initiator_username)
        ChatMessage.objects.create(
            session=self.chat_session,
            sender=sender,
            content=content,
        )

    @sync_to_async
    def update_typing_indicator(self, is_typing):
        # Update typing indicator
        user = User.objects.get(username=self.initiator_username)
        TypingIndicator.objects.update_or_create(
            session=self.chat_session,
            user=user,
            defaults={"is_typing": is_typing},
        )

    @sync_to_async
    def end_chat_session(self):
        # Mark the chat session as ended
        self.chat_session.active = False
        self.chat_session.end_time = now()
        self.chat_session.save()
