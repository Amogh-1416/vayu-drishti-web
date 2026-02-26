import json
import asyncio
import websockets

uri = "ws://127.0.0.1:8000/ws/telemetry/"

async def fly_drone():
    # Heartbeat settings prevent the connection from timing out
    async with websockets.connect(
        uri, 
        open_timeout=20,
        ping_interval=20, 
        ping_timeout=10 
    ) as websocket:
        print("✅ Connected to Vayu Drishti")
        lat, lon = 17.3850, 78.4867
        while True:
            lat += 0.0001
            lon += 0.0001
            payload = {
                "latitude": lat,
                "longitude": lon,
                "altitude": 60.0
            }
            await websocket.send(json.dumps(payload))
            print(f"Sent: {lat}, {lon}")
            await asyncio.sleep(1.0) # Stable update rate

try:
    asyncio.run(fly_drone())
except Exception as e:
    print(f"Connection lost: {e}")