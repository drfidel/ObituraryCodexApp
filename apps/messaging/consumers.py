import json
from channels.generic.websocket import AsyncWebsocketConsumer


class LiveCondolenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.slug = self.scope["url_route"]["kwargs"]["slug"]
        self.room_group_name = f"tribute_{self.slug}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        payload = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_message",
                "message": payload.get("message", ""),
                "user": payload.get("user", "anonymous"),
            },
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps(event))
