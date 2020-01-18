"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CHANNELS ROUTING
- tutorial has app/routing.py and chat/routing.py
- combined both into one file
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.urls import re_path
import movies.consumers as MC
#import recommend.consumers as RC

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', MC.ChatConsumer),
    re_path(r'ws/movies/$', MC.ChatConsumer),
]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CHANNELS APPLICATION
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

