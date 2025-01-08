import json
import logging
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from myapp.models import Person
from .models import ChatSession, ChatMessage, TypingIndicator
from datetime import datetime

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
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

        except ObjectDoesNotExist as e:
            logger.error(f"Error connecting: {e}")
            await self.close()

        except Exception as e:
            logger.error(f"Unexpected error during connection: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Remove this connection from the room group
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

            # End the session if necessary
            await self.end_chat_session()

        except Exception as e:
            logger.error(f"Error during disconnect: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")
            content = text_data_json.get("content")

            # Handle chat messages
            if message_type == "chat_message":
                if not content:
                    raise ValueError("Message content is required.")

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

            # Handle WebRTC signaling messages (offer, answer, ice-candidate)
            elif message_type == "offer":
                offer_sdp = text_data_json.get("sdp")
                if offer_sdp:
                    await self.send_offer(offer_sdp)
            elif message_type == "answer":
                answer_sdp = text_data_json.get("sdp")
                if answer_sdp:
                    await self.send_answer(answer_sdp)
            elif message_type == "ice-candidate":
                ice_candidate = text_data_json.get("candidate")
                if ice_candidate:
                    await self.send_ice_candidate(ice_candidate)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON data received: {e}")
            await self.send(text_data=json.dumps({
                "error": "Invalid message format."
            }))
        except ValueError as e:
            logger.error(f"Value error: {e}")
            await self.send(text_data=json.dumps({
                "error": str(e)
            }))
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await self.send(text_data=json.dumps({
                "error": "An unexpected error occurred."
            }))

    async def chat_message(self, event):
        try:
            # Send the chat message to the WebSocket client
            await self.send(text_data=json.dumps({
                "type": "chat_message",
                "sender": event["sender"],
                "content": event["content"],
            }))
        except Exception as e:
            logger.error(f"Error sending chat message: {e}")

    async def typing_indicator(self, event):
        try:
            # Send the typing indicator to the WebSocket client
            await self.send(text_data=json.dumps({
                "type": "typing",
                "user": event["user"],
                "is_typing": event["is_typing"],
            }))
        except Exception as e:
            logger.error(f"Error sending typing indicator: {e}")

    async def send_offer(self, offer_sdp):
        try:
            # Broadcast the WebRTC offer to the recipient
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "webrtc_offer",
                    "sender": self.initiator_username,
                    "sdp": offer_sdp,
                },
            )
        except Exception as e:
            logger.error(f"Error sending WebRTC offer: {e}")

    async def send_answer(self, answer_sdp):
        try:
            # Broadcast the WebRTC answer to the recipient
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "webrtc_answer",
                    "sender": self.initiator_username,
                    "sdp": answer_sdp,
                },
            )
        except Exception as e:
            logger.error(f"Error sending WebRTC answer: {e}")

    async def send_ice_candidate(self, ice_candidate):
        try:
            # Broadcast the WebRTC ICE candidate to the recipient
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "webrtc_ice_candidate",
                    "sender": self.initiator_username,
                    "candidate": ice_candidate,
                },
            )
        except Exception as e:
            logger.error(f"Error sending ICE candidate: {e}")

    @sync_to_async
    def get_or_create_chat_session(self):
        try:
            # Ensure a ChatSession exists between the two users
            initiator = User.objects.get(username=self.initiator_username)
            recipient = User.objects.get(username=self.recipient_username)

            session, _ = ChatSession.objects.get_or_create(
                initiator=initiator,
                recipient=recipient,
                active=True,
            )
            return session
        except ObjectDoesNotExist as e:
            logger.error(f"Error fetching users for chat session: {e}")
            raise e  # Reraise the error to be handled by the consumer
        except Exception as e:
            logger.error(f"Unexpected error creating chat session: {e}")
            raise e

    @sync_to_async
    def save_message(self, content):
        try:
            # Save the message in the database
            sender = User.objects.get(username=self.initiator_username)
            ChatMessage.objects.create(
                session=self.chat_session,
                sender=sender,
                content=content,
            )
        except ObjectDoesNotExist as e:
            logger.error(f"Error saving message, user not found: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error saving message: {e}")
            raise e

    @sync_to_async
    def update_typing_indicator(self, is_typing):
        try:
            # Update typing indicator
            user = User.objects.get(username=self.initiator_username)
            TypingIndicator.objects.update_or_create(
                session=self.chat_session,
                user=user,
                defaults={"is_typing": is_typing},
            )
        except ObjectDoesNotExist as e:
            logger.error(f"Error updating typing indicator, user not found: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error updating typing indicator: {e}")
            raise e

    @sync_to_async
    def end_chat_session(self):
        try:
            # Mark the chat session as ended
            self.chat_session.active = False
            self.chat_session.end_time = datetime.now()
            self.chat_session.save()
        except Exception as e:
            logger.error(f"Error ending chat session: {e}")
            raise e
