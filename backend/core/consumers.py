import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.gis.geos import Point
from .models import Drone
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DroneTelemetryConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_counter = 0
    
    async def connect(self):
        # Group all connected users (like the React map) into a single "room"
        self.room_group_name = "deone_telemetry"

        # Join the room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the Wensocket connection
        await self.accept()
        print("Websocket Connected: Dashboard is listening for drones")

    async def disconnect(self, close_code):

        # Leave the room when map is closed
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Websocket disconnected")

    # This triggers the millisecond drone sends a JSON payload to the server
    async def receive(self, text_data):
        payload = json.loads(text_data)

        # Broadcast the exact payload data to everyone connected to drone_telemetry room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_telemetry',
                'data': payload
            }
        )
        self.message_counter += 1

        if self.message_counter >= 50:
            await self.save_drone_location(payload)
            self.message_counter = 0

    # The actual broadcasting function that pushes data to browser
    async def broadcast_telemetry(self, event):
        await self.send(text_data=json.dumps({
            'telemetry': event['data']
        }))

    @database_sync_to_async
    def save_drone_location(self, payload):
        drone_name = payload.get('drone_id')
        lat = payload.get('lat')
        lng = payload.get('lng')

        if drone_name and lat and lng:
            current_location = Point(lng, lat)

            drone, created = Drone.objects.update_or_create(
                name = drone_name,
                defaults={'location': current_location}
            )
            print(f"Throttled save: Updated {drone_name} location in Postgres")




class DisasterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the "disaster_data" group defined in your bridge script
        await self.channel_layer.group_add("disaster_data", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("disaster_data", self.channel_name)

    # This name MUST match the "type" in bridge_listener.py (send_disaster_update)
    async def send_disaster_update(self, event):
        payload = event["payload"]

        # Send the actual JSON to the React/Vue frontend
        await self.send(text_data=json.dumps(payload))
