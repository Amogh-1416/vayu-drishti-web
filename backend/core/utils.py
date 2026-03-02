import math

def generate_mock_telemetry(start_lat, start_lng, duration_sec, bearing_degrees=90, speed_mps=5):
    """
    Generates a fake drone flight path for Vayu-Drishti.
    
    :param start_lat: Anchor Latitude (e.g., Disaster Epicenter)
    :param start_lng: Anchor Longitude
    :param duration_sec: Length of the video in seconds (e.g., 20)
    :param bearing_degrees: Direction of flight (0=N, 90=E, 180=S, 270=W)
    :param speed_mps: Drone speed in meters per second (5 m/s is typical for scanning)
    :return: List of dictionaries mapping seconds to coordinates.
    """
    telemetry = []
    
    # Earth's radius in meters
    R = 6378137.0 

    # Generate a coordinate for every second, including second 0
    for sec in range(int(duration_sec) + 1): 
        # Calculate distance traveled so far
        distance = speed_mps * sec
        
        # Convert inputs to radians for the math module
        lat1 = math.radians(start_lat)
        lon1 = math.radians(start_lng)
        brng = math.radians(bearing_degrees)
        
        # Destination point formula
        lat2 = math.asin(
            math.sin(lat1) * math.cos(distance / R) +
            math.cos(lat1) * math.sin(distance / R) * math.cos(brng)
        )
        
        lon2 = lon1 + math.atan2(
            math.sin(brng) * math.sin(distance / R) * math.cos(lat1),
            math.cos(distance / R) - math.sin(lat1) * math.sin(lat2)
        )
        
        # Append the calculated point for this specific second
        telemetry.append({
            "timestamp_sec": float(sec),
            "lat": round(math.degrees(lat2), 7),
            "lng": round(math.degrees(lon2), 7),
            "altitude_m": 120.0  # Static safe altitude for mock data
        })
        
    return telemetry

# --- Example Usage ---
# Let's say you pick a flooded area in Assam as your starting point for a 20s video.
# mock_data = generate_mock_telemetry(26.1433, 91.7898, 20)
# print(mock_data)