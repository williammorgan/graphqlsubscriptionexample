import asyncio

import channels_graphql_ws

import temperatureapp.schema

class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = temperatureapp.schema.schema