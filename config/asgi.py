import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from auction.routing import websocket_urlpatterns
from auction.middlewares import WebSocketJWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django_asgi_app = get_asgi_application()

import auction.routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": 
            WebSocketJWTAuthMiddleware(
                URLRouter(
                    auction.routing.websocket_urlpatterns,
                )
            ),
    }
)
