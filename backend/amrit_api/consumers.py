import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'telemetry'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Relay data to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'telemetry_message',
                'message': data.get('message', data)
            }
        )

    async def telemetry_message(self, event):
        # This sends the data to your browser
        await self.send(text_data=json.dumps(event['message']))