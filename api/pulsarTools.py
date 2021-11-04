"""
    pulsarTools.py
"""

import os
import pulsar



try:
    STREAMING_TENANT = os.environ['STREAMING_TENANT']
    STREAMING_NAMESPACE = os.environ['STREAMING_NAMESPACE']
    STREAMING_TOPIC = os.environ['STREAMING_TOPIC']
    service_url = os.environ['SERVICE_URL']
    trust_certs = os.environ['TRUST_CERTS']
    token = os.environ['ASTRA_TOKEN']
    #
    client = pulsar.Client(service_url,
                           authentication=pulsar.AuthenticationToken(token),
                           tls_trust_certs_file_path=trust_certs)
except KeyError:
    raise KeyError('Environment variables not detected. Perhaps you forgot to '
          'source the ".env" file with ". ../.env" ?')

streamingTopic = 'persistent://{tenant}/{namespace}/{topic}'.format(
    tenant=STREAMING_TENANT,
    namespace=STREAMING_NAMESPACE,
    topic=STREAMING_TOPIC,
)


consumerCache = {}


def getPulsarClient():
    return client


def getConsumer(clientID, puClient):
    if clientID not in consumerCache:
        pulsarSubscription = f'xsub_{clientID}'
        consumerCache[clientID] = puClient.subscribe(streamingTopic,
                                                     pulsarSubscription)
    #
    return consumerCache[clientID]


def getProducer(puClient):
    return puClient.create_producer(streamingTopic)


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
