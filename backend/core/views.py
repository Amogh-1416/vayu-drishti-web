from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage

from .models import SurvivorCluster, DamageReport
from .serializers import SurvivorClusterSerializer, DamageReportSerializer
from .utils import generate_mock_telemetry
from celery import current_app
from shapely.geometry import Point, box, Polygon
from shapely.strtree import STRtree
import networkx as nx
import numpy as np

# --- Your Existing ViewSets (For the Map) ---

class SurvivorClusterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SurvivorCluster.objects.all()
    serializer_class = SurvivorClusterSerializer

class DamageReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DamageReport.objects.all()
    serializer_class = DamageReportSerializer


# --- New View (For Uploading Drone Footage) ---

@api_view(['POST'])
def handle_video_upload(request):
    """
    Accepts a video upload from the frontend, generates mock telemetry,
    and pushes the task to the vayu-drishti-ml Celery queue.
    """
    # 1. Grab the file and metadata from the frontend POST request
    video_file = request.FILES.get('video')
    
    # Using default fallbacks just in case the frontend misses them
    duration_sec = float(request.data.get('duration', 20.0))
    disaster_lat = float(request.data.get('lat', 26.1433)) # Default test coordinate
    disaster_lng = float(request.data.get('lng', 91.7898)) 

    if not video_file:
        return Response({"error": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Save the file so the ML service can find it
    # This saves it to your MEDIA_ROOT folder
    file_name = default_storage.save(f"drone_videos/{video_file.name}", video_file)
    absolute_file_path = default_storage.path(file_name)

    # 3. Generate the fake flight path using the utils.py script we made
    telemetry_data = generate_mock_telemetry(
        start_lat=disaster_lat,
        start_lng=disaster_lng,
        duration_sec=duration_sec
    )

    # 4. Push the job to the Redis queue for your ML worker to pick up
    task = current_app.send_task(
        'process_drone_video',  # Ensure this matches the @shared_task name in your ML service
        kwargs={
            'video_path': absolute_file_path, 
            'telemetry_data': telemetry_data
        }
    )

    return Response({
        "message": "Video successfully uploaded and sent to ML pipeline.",
        "task_id": str(task.id)
    }, status=status.HTTP_202_ACCEPTED)

# --- Routing API ---

def build_safe_path(start_coord, end_coord, damage_reports):
    """
    Calculates a safe path using Grid-based A* Algorithm avoiding damage zones.
    """
    # Define bounding box for the grid based on start and end points
    min_lng = min(start_coord[0], end_coord[0])
    max_lng = max(start_coord[0], end_coord[0])
    min_lat = min(start_coord[1], end_coord[1])
    max_lat = max(start_coord[1], end_coord[1])

    # Add a padding to the bounding box to allow routing around obstacles
    padding = 0.005 # ~500 meters
    min_lng -= padding
    max_lng += padding
    min_lat -= padding
    max_lat += padding

    # Define grid resolution
    # 0.0001 degrees is roughly 10 meters
    grid_res = 0.0001

    # Create the grid
    lons = np.arange(min_lng, max_lng + grid_res, grid_res)
    lats = np.arange(min_lat, max_lat + grid_res, grid_res)

    # Create Shapely polygons for damage reports
    obstacle_polygons = []

    # Safe classes that should NOT block routing paths
    SAFE_CLASSES = ['BUILDING_NO_DAMAGE', 'ROAD_CLEAR']

    for report in damage_reports:
        if report.damage_type not in SAFE_CLASSES:
            # Damage reports only have a point location in the DB right now based on core/models.py
            # We will create a small buffer around the point to represent the damage zone
            # Buffer of 0.0002 is roughly 20 meters radius
            report_point = Point(report.location.x, report.location.y)
            obstacle_polygons.append(report_point.buffer(0.0002))

    # Build a spatial index for fast obstacle checking
    tree = STRtree(obstacle_polygons)

    # Create the graph
    G = nx.Graph()

    # Find the nearest grid indices to the start and end coordinates
    start_lon_idx = (np.abs(lons - start_coord[0])).argmin()
    start_lat_idx = (np.abs(lats - start_coord[1])).argmin()
    end_lon_idx = (np.abs(lons - end_coord[0])).argmin()
    end_lat_idx = (np.abs(lats - end_coord[1])).argmin()

    # Add nodes to the graph if they don't intersect with obstacles
    for i in range(len(lons)):
        for j in range(len(lats)):
            point = Point(lons[i], lats[j])
            # Check for intersection with obstacles
            if not tree.query(point).size > 0:
                G.add_node((i, j), pos=(lons[i], lats[j]))

    # Add edges to the graph
    for node in G.nodes:
        i, j = node
        # 8-connected grid (horizontal, vertical, diagonal)
        neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1), (i+1, j+1), (i+1, j-1), (i-1, j+1), (i-1, j-1)]
        for neighbor in neighbors:
            if neighbor in G.nodes:
                # Calculate weight (distance)
                p1 = G.nodes[node]['pos']
                p2 = G.nodes[neighbor]['pos']
                dist = np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
                G.add_edge(node, neighbor, weight=dist)

    # If start or end node is not in the graph (e.g., inside an obstacle), find the nearest valid node
    if (start_lon_idx, start_lat_idx) not in G.nodes:
        closest_node = min(G.nodes, key=lambda n: np.sqrt((lons[n[0]] - start_coord[0])**2 + (lats[n[1]] - start_coord[1])**2))
        start_lon_idx, start_lat_idx = closest_node

    if (end_lon_idx, end_lat_idx) not in G.nodes:
        closest_node = min(G.nodes, key=lambda n: np.sqrt((lons[n[0]] - end_coord[0])**2 + (lats[n[1]] - end_coord[1])**2))
        end_lon_idx, end_lat_idx = closest_node

    try:
        # Calculate shortest path using A*
        def heuristic(a, b):
            p1 = G.nodes[a]['pos']
            p2 = G.nodes[b]['pos']
            return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

        path = nx.astar_path(G, (start_lon_idx, start_lat_idx), (end_lon_idx, end_lat_idx), heuristic=heuristic, weight='weight')

        # Convert path back to coordinates
        path_coords = [G.nodes[node]['pos'] for node in path]

        # Replace first and last with exact coordinates if they differ slightly due to grid snap
        path_coords[0] = start_coord
        path_coords[-1] = end_coord

        return path_coords
    except nx.NetworkXNoPath:
        return None


@api_view(['POST'])
def calculate_route(request):
    """
    Calculates a safe route avoiding DamageReports.
    """
    try:
        start_lat = float(request.data.get('start_lat'))
        start_lng = float(request.data.get('start_lng'))
        end_lat = float(request.data.get('end_lat'))
        end_lng = float(request.data.get('end_lng'))
    except (TypeError, ValueError):
        return Response({"error": "Invalid start or end coordinates provided."}, status=status.HTTP_400_BAD_REQUEST)

    start_coord = (start_lng, start_lat)
    end_coord = (end_lng, end_lat)

    # Fetch all damage reports to treat as obstacles
    damage_reports = DamageReport.objects.all()

    # Calculate path
    path_coords = build_safe_path(start_coord, end_coord, damage_reports)

    if path_coords:
        return Response({
            "status": "success",
            "path": [{"lat": lat, "lng": lng} for lng, lat in path_coords]
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "failed",
            "error": "No safe path found."
        }, status=status.HTTP_404_NOT_FOUND)