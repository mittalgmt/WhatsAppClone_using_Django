from django.urls import path
from .consumers import ChatConsumer,PrivatechatConsumer

websocket_urlpatterns = [
    
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
    path('ws/wsc/',PrivatechatConsumer.as_asgi())
]