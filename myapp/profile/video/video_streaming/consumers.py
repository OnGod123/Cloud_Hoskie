import base64
import os
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from video.models import Video

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Handle disconnection logic (if any)
        pass

    async def receive(self, text_data):
        """
        Stream all videos from the database with metadata.
        """
        try:
            # Fetch all video objects from the database
            videos = Video.objects.all()

            for video in videos:
                video_path = video.video_file.path

                # Send metadata to the client
                metadata = {
                    "id": video.id,
                    "title": video.title,
                    "created_at": video.created_at.isoformat(),
                    "updated_at": video.updated_at.isoformat(),
                }
                await self.send(text_data=str(metadata))

                # Stream video data in Base64 chunks
                chunk_size = 1024 * 1024  # 1MB per chunk
                with open(video_path, 'rb') as video_file:
                    while chunk := video_file.read(chunk_size):
                        # Encode the binary data to Base64
                        encoded_chunk = base64.b64encode(chunk).decode('utf-8')
                        await self.send(text_data=encoded_chunk)

                        # Simulate streaming delay for smoother client processing
                        await asyncio.sleep(0.1)

                # Notify the client that streaming for this video has ended
                await self.send(text_data="END_OF_STREAM")

            # Notify that all videos have been streamed
            await self.send(text_data="ALL_VIDEOS_STREAMED")

        except Exception as e:
            # Notify the client of any errors
            await self.send(text_data=f"ERROR: {str(e)}")
