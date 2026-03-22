import json
import asyncio
import websockets
import math
import sys

# Drone WebSocket URL
uri = "ws://127.0.0.1:8000/ws/telemetry/"

def generate_mock_telemetry(start_lat, start_lng, duration_sec, bearing_degrees=90, speed_mps=5):
    """
    Generates a fake drone flight path for Vayu-Drishti.
    """
    telemetry = []
    R = 6378137.0
    for sec in range(int(duration_sec) + 1):
        distance = speed_mps * sec
        lat1 = math.radians(start_lat)
        lon1 = math.radians(start_lng)
        brng = math.radians(bearing_degrees)
        lat2 = math.asin(
            math.sin(lat1) * math.cos(distance / R) +
            math.cos(lat1) * math.sin(distance / R) * math.cos(brng)
        )
        lon2 = lon1 + math.atan2(
            math.sin(brng) * math.sin(distance / R) * math.cos(lat1),
            math.cos(distance / R) - math.sin(lat1) * math.sin(lat2)
        )
        telemetry.append({
            "timestamp_sec": float(sec),
            "latitude": round(math.degrees(lat2), 7),
            "longitude": round(math.degrees(lon2), 7),
            "altitude": 120.0
        })
    return telemetry


async def fly_drone(start_lat, start_lng, duration_sec, speed_mps, bearing_degrees):
    flight_path = generate_mock_telemetry(
        start_lat,
        start_lng,
        duration_sec,
        bearing_degrees,
        speed_mps
    )

    print(f"🚁 Initiating mock flight path starting from {start_lat}, {start_lng} for {duration_sec} seconds...")

    try:
        async with websockets.connect(
            uri,
            open_timeout=30,
            ping_interval=10,
            ping_timeout=20,
            close_timeout=10
        ) as websocket:
            print("✅ Connected to Vayu Drishti Telemetry System")

            for point in flight_path:
                payload = {
                    "latitude": point["latitude"],
                    "longitude": point["longitude"],
                    "altitude": point["altitude"]
                }
                await websocket.send(json.dumps(payload))
                print(f"📡 Sent Telemetry: Lat={point['latitude']}, Lng={point['longitude']}, Alt={point['altitude']}")

                # Wait 1 second before sending the next point to simulate real-time
                await asyncio.sleep(1.0)

            print("🏁 Drone has completed its flight path.")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"❌ Connection to WebSocket was closed unexpectedly: {e}")
    except Exception as e:
        print(f"❌ Connection lost or failed: {e}")

if __name__ == "__main__":
    # You can customize these defaults
    START_LAT = 17.3850
    START_LNG = 78.4867
    DURATION = 60 # seconds
    SPEED_MPS = 5 # meters per second
    BEARING = 90 # degrees (East)

    if len(sys.argv) > 1:
        try:
            START_LAT = float(sys.argv[1])
            START_LNG = float(sys.argv[2])
            DURATION = int(sys.argv[3])
        except ValueError:
            print("Usage: python fake_drone.py [START_LAT START_LNG DURATION_SEC]")
            sys.exit(1)

    try:
        asyncio.run(fly_drone(START_LAT, START_LNG, DURATION, SPEED_MPS, BEARING))
    except KeyboardInterrupt:
        print("\n🛑 Mock drone flight stopped by user.")