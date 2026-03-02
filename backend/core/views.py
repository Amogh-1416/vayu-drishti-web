from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage

from .models import SurvivorCluster, DamageReport
from .serializers import SurvivorClusterSerializer, DamageReportSerializer
from .utils import generate_mock_telemetry
from celery import current_app

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