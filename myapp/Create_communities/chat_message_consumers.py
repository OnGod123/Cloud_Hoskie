import json
import base64
import os
from django.core.files.base import ContentFile
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from app.models import ChatMessage, ChatSession, Person
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        On connection, add the user to the session's group.
        """
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f"chat_session_{self.session_id}"

        # Add the WebSocket to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        On disconnection, remove the user from the session's group.
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handle incoming messages from WebSocket clients.
        """
        data = json.loads(text_data)
        action = data.get("action")

        if action == "send_message":
            await self.handle_send_message(data)
        elif action == "edit_message":
            await self.handle_edit_message(data)
        elif action == "delete_message":
            await self.handle_delete_message(data)
        else:
            await self.send(json.dumps({
                "error": "Invalid action"
            }))

    async def handle_send_message(self, data):
        """
        Broadcast a new message to the group.
        """
        session_id = data.get("session_id")
        sender_id = data.get("sender_id")
        content = data.get("content", "")
        encoded_image = data.get("image")  # Base64 string of the image, if present

        # Validate and save message
        session = await sync_to_async(get_object_or_404)(ChatSession, id=session_id)
        sender = await sync_to_async(get_object_or_404)(Person, id=sender_id)

        # If an image is provided, decode and store it
        image_path = None
        if encoded_image:
            # Decode the base64 image and save it to the media path
            format, imgstr = encoded_image.split(";base64,")
            ext = format.split("/")[-1]  # Extract image extension (e.g., jpg, png)
            image_name = f"{sender.id}_{session_id}_{int(session.participants.count())}.{ext}"
            image_path = os.path.join("chat_images", image_name)
            decoded_image = ContentFile(base64.b64decode(imgstr), name=image_name)

            # Save the decoded image
            chat_message = await sync_to_async(ChatMessage.objects.create)(
                session=session,
                sender=sender,
                content=content,  # Optional text
                image=decoded_image
            )
        else:
            # Save message without an image
            chat_message = await sync_to_async(ChatMessage.objects.create)(
                session=session,
                sender=sender,
                content=content
            )

        # Broadcast the new message
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message_id": chat_message.id,
                "sender": sender.name,
                "content": content,
                "image": chat_message.image.url if chat_message.image else None,  # Include image URL if available
                "timestamp": str(chat_message.timestamp),
                "action": "send_message",
            }
        )

    async def handle_edit_message(self, data):
        """
        Allow the sender to edit a message they’ve sent.
        Broadcast the change to all clients in the group.
        """
        message_id = data.get("message_id")
        new_content = data.get("content")
        sender_id = data.get("sender_id")

        try:
            chat_message = await sync_to_async(ChatMessage.objects.get)(id=message_id)

            # Validate ownership
            if chat_message.sender.id != sender_id:
                await self.send(json.dumps({"error": "You can only edit your own messages"}))
                return

            # Update the message content
            chat_message.content = new_content
            await sync_to_async(chat_message.save)()

            # Broadcast the updated message
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message_id": chat_message.id,
                    "sender": chat_message.sender.name,
                    "content": new_content,
                    "image": chat_message.image.url if chat_message.image else None,  # Include image if present
                    "timestamp": str(chat_message.timestamp),
                    "action": "edit_message",
                }
            )

        except ChatMessage.DoesNotExist:
            await self.send(json.dumps({"error": "Message not found"}))

    async def handle_delete_message(self, data):
        """
        Allow the sender to delete a message they’ve sent.
        Broadcast the deletion to all clients in the group.
        """
        message_id = data.get("message_id")
        sender_id = data.get("sender_id")

        try:
            chat_message = await sync_to_async(ChatMessage.objects.get)(id=message_id)

            # Validate ownership
            if chat_message.sender.id != sender_id:
                await self.send(json.dumps({"error": "You can only delete your own messages"}))
                return

            # Delete the message
            await sync_to_async(chat_message.delete)()

            # Broadcast the deletion
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message_id": message_id,
                    "action": "delete_message",
                }
            )

        except ChatMessage.DoesNotExist:
            await self.send(json.dumps({"error": "Message not found"}))

    async def chat_message(self, event):
        """
        Broadcast chat messages (new, edited, or deleted) to all WebSocket clients.
        """
        await self.send(text_data=json.dumps({
            "action": event["action"],
            "message_id": event.get("message_id"),
            "sender": event.get("sender"),
            "content": event.get("content"),
            "image": event.get("image"),  # Add image URL if provided
            "timestamp": event.get("timestamp"),
        }))