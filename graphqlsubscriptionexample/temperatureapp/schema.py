import asyncio
import datetime
import random

import channels_graphql_ws
import graphene
from graphene_django import DjangoObjectType

from temperatureapp.models import TemperatureMeasurement

class TemperatureMeasurementType(DjangoObjectType):
    class Meta:
        model = TemperatureMeasurement
        fields = ("timestamp", "value")

    unit = graphene.String()

    def resolve_unit(self, info):
        return "Degrees Celsius"


class CurrentTemperatureSubscription(channels_graphql_ws.Subscription):
    temperature = graphene.Field(TemperatureMeasurementType)

    @staticmethod
    def subscribe(root, info):
        return ['temperature_group']

    @staticmethod
    def publish(payload, info):
        return CurrentTemperatureSubscription(
            temperature=payload,
        )


class Query(graphene.ObjectType):
    current_temperature = graphene.Field(TemperatureMeasurementType)

    @staticmethod
    def resolve_current_temperature(parent, info):
        return TemperatureMeasurement.objects.order_by("timestamp").last()


class Subscription(graphene.ObjectType):
    current_temperature_subscribe = CurrentTemperatureSubscription.Field()


schema = graphene.Schema(query=Query, subscription=Subscription)
