"""
ASGI config for graphqlsubscriptionexample project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import channels.routing
from django.urls import path
from django.core.asgi import get_asgi_application
from temperatureapp.graphql_ws_consumer import GraphqlWsConsumer

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'graphqlsubscriptionexample.settings'
)

application = channels.routing.ProtocolTypeRouter({
    "https": get_asgi_application(),
    "websocket": channels.routing.URLRouter([
        path("graphql/", GraphqlWsConsumer)
    ]),
})
