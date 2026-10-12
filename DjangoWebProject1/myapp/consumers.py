
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope["url_route"]["kwargs"]["room"]
        self.group_name = f"chat_{self.room}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "percentage.update",
                "wpp": data["wpp"],
                "lpp": data["lpp"],
                "dpp": data["dpp"],
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "wpp": event["wpp"],
                "lpp": event["lpp"],
                "dpp": event["dpp"],
            })
        )

