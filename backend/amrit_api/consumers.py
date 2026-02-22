import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_sending = True
        # Fulfills sub-second update requirement from Issue #10
        asyncio.create_task(self.broadcast_updates())

    async def disconnect(self, close_code):
        self.keep_sending = False

    async def broadcast_updates(self):
        while self.keep_sending:
            data = {
                "latitude": 17.3850 + random.uniform(-0.001, 0.001),
                "longitude": 78.4867 + random.uniform(-0.001, 0.001),
                "altitude": random.uniform(50, 60)
            }
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(0.2) # 5 updates per second