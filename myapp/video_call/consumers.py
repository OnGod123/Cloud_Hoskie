import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from myapp.video_call.models import VideoCall
from myapp.models import Person
from asgiref.sync import sync_to_async


class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
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
            initiator = await sync_to_async(Person.objects.get)(username=self.initiator_username)
            recipient = await sync_to_async(Person.objects.get)(username=self.recipient_username)

            # Create a new call instance
            await sync_to_async(VideoCall.objects.create)(
                initiator=initiator,
                recipient=recipient,
                start_time=timezone.now(),
                status='active'
            )

            # Start periodic pinging
            self.ping_task = asyncio.create_task(self.send_ping())

        except Person.DoesNotExist as e:
            # Log the error and notify the client that one of the users does not exist
            print(f"Error: {e}")
            await self.close(code=4001)  # Close with custom error code if user is not found

        except Exception as e:
            # Handle unexpected errors
            print(f"Unexpected error during connection: {e}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred during the connection. Please try again later.'
            }))
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Update the VideoCall status to 'ended' when the WebSocket disconnects
            await sync_to_async(VideoCall.objects.filter(
                initiator__username=self.initiator_username,
                recipient__username=self.recipient_username,
                status='active'
            ).update)(end_time=timezone.now(), status='ended')

            # Cancel the ping task when disconnecting
            if hasattr(self, 'ping_task'):
                self.ping_task.cancel()

            # Leave the room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        except Exception as e:
            # Log the error and notify the client if any error occurs during disconnection
            print(f"Error during disconnect: {e}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred while disconnecting the call.'
            }))

    async def receive(self, text_data):
        try:
            # This will handle any message sent from the client
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            data = text_data_json.get('data')

            if not message_type or not data:
                await self.send(text_data=json.dumps({
                    'error': 'Malformed message received.'
                }))
                return

            # Handle different message types for WebRTC signaling
            if message_type == 'offer':
                # Handle SDP offer from initiator
                await self.handle_offer(data)
            elif message_type == 'answer':
                # Handle SDP answer from recipient
                await self.handle_answer(data)
            elif message_type == 'candidate':
                # Handle ICE candidate
                await self.handle_candidate(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'data': data  # Echo back the ping data if needed
                }))
            else:
                # If the message type is unknown, notify the client
                await self.send(text_data=json.dumps({
                    'error': 'Unknown message type.'
                }))

        except json.JSONDecodeError as e:
            # Handle invalid JSON format error
            print(f"Invalid JSON format: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format. Please check the data structure.'
            }))

        except Exception as e:
            # Log any unexpected errors
            print(f"Unexpected error while receiving data: {e}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred while processing the message.'
            }))

    async def webrtc_message(self, event):
        try:
            message_type = event['message_type']
            data = event['data']

            # Send the message to the WebSocket client
            await self.send(text_data=json.dumps({
                message_type: data
            }))

        except KeyError as e:
            # Handle missing key errors in the message data
            print(f"Missing key in event data: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Invalid message structure received.'
            }))

        except Exception as e:
            # Log any unexpected errors during broadcasting
            print(f"Unexpected error while sending message: {e}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred while sending the message.'
            }))

    async def send_ping(self):
        while True:
            try:
                # Send periodic ping messages
                await self.send(text_data=json.dumps({
                    'type': 'ping',
                    'data': 'ping'  # Customize this payload if needed
                }))
                await asyncio.sleep(10)  # Ping every 10 seconds
            except asyncio.CancelledError:
                # Stop sending pings when the WebSocket connection is closed
                break

            except Exception as e:
                # Handle any unexpected errors during pinging
                print(f"Error during pinging: {e}")
                await self.send(text_data=json.dumps({
                    'error': 'An error occurred while sending the ping.'
                }))
                break

    async def handle_offer(self, offer_data):
        try:
            # Forward the offer to the recipient peer
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_message',
                    'message_type': 'offer',
                    'data': offer_data
                }
            )

        except Exception as e:
            print(f"Error handling offer: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Error handling offer.'
            }))

    async def handle_answer(self, answer_data):
        try:
            # Forward the answer to the initiator peer
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_message',
                    'message_type': 'answer',
                    'data': answer_data
                }
            )

        except Exception as e:
            print(f"Error handling answer: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Error handling answer.'
            }))

    async def handle_candidate(self, candidate_data):
        try:
            # Forward the ICE candidate to the other peer
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_message',
                    'message_type': 'candidate',
                    'data': candidate_data
                }
            )

        except Exception as e:
            print(f"Error handling candidate: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Error handling candidate.'
            }))
