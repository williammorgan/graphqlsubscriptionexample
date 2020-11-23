
# GraphQL Subscription Example #

The point of this project is to demonstrate the use of GraphQL subscriptions over websockets in Django as simply as possible.

It uses a pretend temperature sensor, which just generates a plausible random number once a second.  This number is saved to the database and reported to all the subscribers.  Subscribers all see the same values, and GraphQL queries made at that time see the same value as the subscribers.

This uses the Django built in debug webserver instead of a production ready webserver, so consider it for demonstration purposes only.

## Setting It Up ##

The simplest way is to run it with docker and map the exposed port 8000.  In a fresh checkout, run:

    docker build -t graphqlsubscriptionexample .
    docker run -p8000:8000 graphqlsubscriptionexample

To run without docker, you should make a virtualenv in a location of your choosing (below assumes ~/.venvs) and install the dependencies. This project was only tested with python3.8.

    python3.8 -m venv ~/.venvs/graphqlsubscriptionexample
    source ~/.venvs/graphqlsubscriptionexample/bin/activate
    pip install --editable .
    python graphqlsubscriptionexample/manage.py runserver 0:8001

If you want to have the exact versions of libraries I tested with, you can use `pip install -r requirements.txt` instead of the other `pip install` step above.  That is what the Dockerfile does.

You can run the tests with:

    pytest

## Using It ##

Once it is running, you can use the built in GraphiQL application served at `127.0.0.1:8000/graphql/` to issue query and subscription requests like these from your browser:

    query one{
      currentTemperature{
        timestamp
  	    value
        unit
      }
    }

    subscription two{
      currentTemperatureSubscribe{
        temperature{
          timestamp
          value
          unit
        }
      }
    }

## Some Notes ##

I used this library for the websocket subscriptions:  
https://github.com/datadvance/DjangoChannelsGraphqlWs

becasue of a maintenance issue with this one:  
https://github.com/graphql-python/graphql-ws/issues/30

I used python3.8 instead of 3.9 becasue of this graphene issue:  
https://github.com/graphql-python/graphene/issues/1055