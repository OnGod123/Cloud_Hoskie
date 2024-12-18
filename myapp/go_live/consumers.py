import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LiveSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f"live_session_{self.session_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if 'type' in data:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "broadcast_signal", "data": data}
                )
        except Exception as e:
            await self.send(text_data=json.dumps({"type": "error", "message": str(e)}))

    async def broadcast_signal(self, event):
        await self.send(text_data=json.dumps(event["data"]))
