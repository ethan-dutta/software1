# import json
# from channels.generic.websocket import (
#    AsyncWebsocketConsumer,
# )
# from channels.db import database_sync_to_async

# class ChatConsumer(AsyncWebsocketConsumer):
#    async def connect(self):
#        self.room = self.scope["url_route"]["kwargs"]["room"]
#        self.group_name = f"chat_{self.room}"
#        await self.channel_layer.group_add(
#            self.group_name, self.channel_name
#        )
#        await self.accept()

#    async def disconnect(self, close_code):
#        await self.channel_layer.group_discard(
#            self.group_name, self.channel_name
#        )
#    async def receive(self, text_data):
#        data = json.loads(text_data)
#        await self.channel_layer.group_send(
#            self.group_name,
#            {"type": "chat.message",
#             "message": data["message"],
#             "user": self.scope["user"].username},
#        )

#    async def chat_message(self, event):
#        await self.send(text_data=json.dumps({
#            "message": event["message"],
#            "user": event["user"],
#        }))
#    async def receive(self, text_data):
#        data = json.loads(text_data)
#        # This query blocks ALL connections on this worker
#        msg = Message.objects.create(
#            room=self.room, text=data["message"]
#        )

#    # RIGHT -- runs in a thread pool
#    async def receive(self, text_data):
#        data = json.loads(text_data)
#        msg = await database_sync_to_async(
#            Message.objects.create
#        )(room=self.room, text=data["message"])

#    @database_sync_to_async
#    def save_message(self, room, user, text):
#        return Message.objects.create(
#            room=room, user=user, text=text
#        )

#    @database_sync_to_async
#    def get_recent_messages(self, room, limit=50):
#        return list(
#            Message.objects.filter(room=room)
#            .order_by("-created")[:limit]
#        )
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
                "type": "chat.message",
                "message": data["message"],
                "user": self.scope["user"].username,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "user": event["user"],
            })
        )

