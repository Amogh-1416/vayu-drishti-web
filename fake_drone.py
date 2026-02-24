import asyncio
import websockets
import json

async def fly_drone():
    uri = "ws://127.0.0.1:8000/ws/telemetry/"

    async with websockets.connect(uri) as websocket:
        print("Drone Alpha connected to command center")


        lat = 18.79
        lng = 79.49

        while True:
            lat += 0.0001
            lng += 0.0001

            payload = {
                "drone_id": "Alpha-1",
                "lat": lat,
                "lng": lng,
                "altitude": 120
            }

            await websocket.send(json.dumps(payload))

            print(f"Sent: {lat:.4f}, {lng:.4f}")

            await asyncio.sleep(0.1)

asyncio.run(fly_drone())