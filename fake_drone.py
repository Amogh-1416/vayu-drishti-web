import json
import asyncio
import websockets

uri = "ws://127.0.0.1:8000/ws/telemetry/"

async def fly_drone():
    async with websockets.connect(
        uri, 
        ping_interval=10,  
        ping_timeout=20,   
        open_timeout=20
    ) as websocket:
        print("🚀 Simulator connected and streaming...")
        
        
        step = 0
        base_lat, base_lon = 17.3850, 78.4867
        
        while True:
            
            lat = base_lat + (step * 0.0002)
            lon = base_lon + (step * 0.0002)
            
            payload = {
                "latitude": round(lat, 6), 
                "longitude": round(lon, 6), 
                "altitude": 60.0
            }
            
            try:
                await websocket.send(json.dumps(payload))
                print(f"📡 Sent Telemetry Step {step}: {lat:.5f}, {lon:.5f}")
                step += 1
                await asyncio.sleep(1.0) 
            except Exception as e:
                print(f"⚠️ Connection Lost at step {step}: {e}")
                break

if __name__ == "__main__":
    asyncio.run(fly_drone())