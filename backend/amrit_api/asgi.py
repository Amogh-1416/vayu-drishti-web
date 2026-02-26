# vayu_drishti/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import amrit_api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vayu_drishti.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            amrit_api.routing.websocket_urlpatterns
        )
    ),
})