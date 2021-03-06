"""
    pulsarTools.py
"""

import os
import pulsar
from dotenv import load_dotenv


load_dotenv()
try:
    STREAMING_TENANT = os.environ['STREAMING_TENANT']
    STREAMING_NAMESPACE = os.environ['STREAMING_NAMESPACE']
    STREAMING_TOPIC = os.environ['STREAMING_TOPIC']
    STREAMING_SERVICE_URL = os.environ['STREAMING_SERVICE_URL']
    TRUST_CERTS = os.environ['TRUST_CERTS']
    ASTRA_STREAMING_TOKEN = os.environ['ASTRA_STREAMING_TOKEN']
    #
    client = pulsar.Client(
        STREAMING_SERVICE_URL,
        authentication=pulsar.AuthenticationToken(ASTRA_STREAMING_TOKEN),
        tls_trust_certs_file_path=TRUST_CERTS,
    )
except KeyError:
    raise KeyError('Environment variables not detected. Perhaps you forgot to '
                   'prepare the .env file ?')

streamingTopic = 'persistent://{tenant}/{namespace}/{topic}'.format(
    tenant=STREAMING_TENANT,
    namespace=STREAMING_NAMESPACE,
    topic=STREAMING_TOPIC,
)


# Pulsar producer/consumer caches
# (for parsimonious allocation of resources)
consumerCache = {}
cachedProducer = None


def getPulsarClient():
    return client


def getConsumer(clientID, puClient):
    global consumerCache
    #
    if clientID not in consumerCache:
        pulsarSubscription = f'sub_{clientID}'
        consumerCache[clientID] = puClient.subscribe(streamingTopic,
                                                     pulsarSubscription)
    #
    return consumerCache[clientID]


def getProducer(puClient):
    global cachedProducer
    #
    if cachedProducer is None:
        cachedProducer = puClient.create_producer(streamingTopic)
    #
    return cachedProducer


def receiveOrNone(consumer, timeout):
    """
    A modified 'receive' function for a Pulsar topic
    that handles timeouts so that when the topic is empty
    it simply returns None.
    """
    try:
        msg = consumer.receive(timeout)
        return msg
    except Exception as e:
        if 'timeout' in str(e).lower():
            return None
        else:
            raise e
