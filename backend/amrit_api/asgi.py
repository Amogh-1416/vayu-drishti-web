import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# Point to amrit_api.routing instead of core.routing
import amrit_api.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amrit_api.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            amrit_api.routing.websocket_urlpatterns
        )
    ),
})