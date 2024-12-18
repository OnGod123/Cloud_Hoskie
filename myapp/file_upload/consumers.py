import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FileUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.room_name = "file_upload_room"
        self.room_group_name = "file_upload_group"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Handles file upload notifications sent through WebSocket.
        """
        try:
            if text_data:
                data = json.loads(text_data)
                file_name = data.get("file_name")
                user = self.scope["user"]

                # Notify the group about the uploaded file
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "file_message",
                        "file_name": file_name,
                        "sender": user.username if user.is_authenticated else "Anonymous",
                    }
                )
        except Exception as e:
            await self.send(text_data=json.dumps({"type": "error", "message": str(e)}))

    async def file_message(self, event):
        """
        Sends the file upload notification to WebSocket clients.
        """
        await self.send(text_data=json.dumps({
            "type": "file",
            "message": f"{event['sender']} uploaded a file: {event['file_name']}",
        }))
