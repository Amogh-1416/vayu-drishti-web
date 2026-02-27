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
        try:
            data = json.loads(text_data)
            payload = data.get('message', data)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'telemetry_message',
                    'message': payload
                }
            )
        except Exception as e:
            print(f"⚠️ Telemetry error: {e}")

    async def telemetry_message(self, event):
        try:
            await self.send(text_data=json.dumps(event['message']))
        except Exception as e:
            print(f"⚠️ Failed to send to browser: {e}")