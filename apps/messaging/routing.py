from django.urls import re_path
from .consumers import LiveCondolenceConsumer

websocket_urlpatterns = [
    re_path(r"ws/tributes/(?P<slug>[-\w]+)/$", LiveCondolenceConsumer.as_asgi()),
]
