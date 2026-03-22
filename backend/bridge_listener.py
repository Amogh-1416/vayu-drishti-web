import os
import sys
import json
import redis

# 1. FORCE WINDOWS TO SEE THE GDAL DLLs
# This must happen before 'django.setup()' to avoid ImproperlyConfigured errors
gdal_path = r'C:\Program Files\PostgreSQL\17\bin'
if gdal_path not in os.environ['PATH']:
    os.environ['PATH'] = gdal_path + os.pathsep + os.environ['PATH']

# 2. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amrit_api.settings')
import django
django.setup()

# 3. Import Geospatial tools, Models, and Channels
from django.contrib.gis.geos import Point 
from core.models import SurvivorCluster, DamageReport
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Initialize Channel Layer for WebSockets
channel_layer = get_channel_layer()

# Color Mapping for Disaster Zone Segmentation based on RescueNet Classes
COLOR_MAP = {
    'WATER': '#1E90FF',                       # Dodger Blue
    'BUILDING_NO_DAMAGE': '#32CD32',          # Lime Green
    'BUILDING_MINOR_DAMAGE': '#FFD700',       # Gold
    'BUILDING_MAJOR_DAMAGE': '#FF8C00',       # Dark Orange
    'BUILDING_TOTAL_DESTRUCTION': '#8B0000',  # Dark Red
    'VEHICLE': '#8A2BE2',                     # Blue Violet
    'ROAD_CLEAR': '#A9A9A9',                  # Dark Gray
    'ROAD_BLOCKED': '#FF0000',                # Red
    'TREE': '#228B22',                        # Forest Green
    'POOL': '#00BFFF',                        # Deep Sky Blue
    'OTHER': '#808080'                        # Gray
}

def start_bridge():
    r = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe('vayu_drishti_video_processing')

    print("🚀 Vayu-Drishti Geo-Bridge is LIVE. Listening for survivor and damage data...")

    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                data = json.loads(message['data'])
                lat = data['location']['lat']
                lng = data['location']['lng']
                
                # Create the GeoDjango Point object
                point = Point(lng, lat, srid=4326)

                # --- 1. PROCESS & SAVE SURVIVORS ---
                if data['humans']:
                    # Save to PostgreSQL
                    SurvivorCluster.objects.create(
                        location=point,
                        estimated_count=len(data['humans']),
                        confidence_score=round(max(h['conf'] for h in data['humans']) * 100, 2),
                        radius_meters=5.0,
                        is_rescued=False
                    )
                    print(f"📍 [SURVIVOR] Saved Geo-Point at {lat}, {lng}")

                    # Broadcast to Frontend via WebSockets
                    async_to_sync(channel_layer.group_send)(
                        "disaster_data",
                        {
                            "type": "send_disaster_update",
                            "payload": {
                                "type": "SURVIVOR",
                                "lat": lat,
                                "lng": lng,
                                "count": len(data['humans']),
                                "color": "#FF0000" # High-visibility Red
                            }
                        }
                    )

                # --- 2. PROCESS & SAVE DAMAGE (ZONE SEGMENTATION) ---
                for infra in data['infrastructure']:
                    # Raw ML String: "Building-Total-Destruction" -> DB Format: "BUILDING_TOTAL_DESTRUCTION"
                    d_type = infra['class'].upper().replace('-', '_').replace(' ', '_')
                    
                    # Validate against your Django Choice Field
                    valid_types = [choice[0] for choice in DamageReport.DAMAGE_TYPES]
                    d_type = d_type if d_type in valid_types else 'OTHER'
                    
                    # Assign segmented color
                    zone_color = COLOR_MAP.get(d_type, '#808080')

                    # Save to PostgreSQL
                    DamageReport.objects.create(
                        location=point,
                        damage_type=d_type,
                        severity_level='HIGH',
                        description="Automated detection via Vayu-Drishti ML"
                    )
                    print(f"🏗️ [DAMAGE] Saved {d_type} Geo-Point at {lat}, {lng}")

                    # Broadcast to Frontend via WebSockets
                    async_to_sync(channel_layer.group_send)(
                        "disaster_data",
                        {
                            "type": "send_disaster_update",
                            "payload": {
                                "type": "DAMAGE",
                                "label": d_type,
                                "lat": lat,
                                "lng": lng,
                                "color": zone_color,
                                "polygon": infra.get('polygon', []) # Normalized segmentation mask
                            }
                        }
                    )

            except Exception as e:
                print(f"❌ Bridge Error: {e}")

if __name__ == "__main__":
    start_bridge()