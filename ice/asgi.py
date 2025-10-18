import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import realtime_chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ice.settings')
django.setup()

# Django's default ASGI app (for HTTP)
django_asgi_app = get_asgi_application()

# Combine Django's HTTP and Channels' WebSocket handlers
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # ✅ handles normal HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            realtime_chat.routing.websocket_urlpatterns
        )
    ),
})
