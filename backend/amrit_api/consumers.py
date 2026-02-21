import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Start sending mock drone data once connected
        self.keep_sending = True
        asyncio.create_task(self.send_telemetry())

    async def disconnect(self, close_code):
        self.keep_sending = False

    async def send_telemetry(self):
        while self.keep_sending:
            # Generate mock coordinates for testing
            data = {
                "latitude": random.uniform(17.3850, 17.4500),
                "longitude": random.uniform(78.4867, 78.5500),
                "altitude": random.uniform(10, 100),
                "velocity": random.uniform(0, 15)
            }
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(1) # Send update every second