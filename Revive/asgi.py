"""
ASGI config for Revive project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Revive.settings')

application = get_asgi_application()


# from django.urls import re_path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from api import consumers  # Import your consumers module

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Revive.settings')  # Replace 'your_project' with your actual project name

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
#             # ... other WebSocket patterns if needed
#         )
#     ),
# })
