from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/telemetry/$', consumers.DroneTelemetryConsumer.as_asgi()),
    re_path(r'ws/disaster/$', consumers.DisasterConsumer.as_asgi()),
]