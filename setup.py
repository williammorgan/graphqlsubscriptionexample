#!/usr/bin/env python
from setuptools import setup

setup(
    name="graphqlsubscriptionexample",
    version="1.0",
    install_requires=[
        "Django",
        "pytest-django",
        "graphene-django",
        "django-channels-graphql-ws",
    ]
)