from django.urls import re_path
from .consumers import TelemetryConsumer

websocket_urlpatterns = [
    # The '?' makes the trailing slash optional to prevent "No route found" errors
    re_path(r'ws/telemetry/?$', TelemetryConsumer.as_asgi()),
]