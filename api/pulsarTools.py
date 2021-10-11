"""
    pulsarTools.py
"""

import os
import pulsar

service_url = os.environ['SERVICE_URL']
trust_certs = os.environ['TRUST_CERTS']
token = os.environ['ASTRA_TOKEN']

client = pulsar.Client(service_url,
                       authentication=pulsar.AuthenticationToken(token),
                       tls_trust_certs_file_path=trust_certs)


def getPulsarClient():
    return client


consumerCache = {}
def getConsumer(clientID, puClient):
    if clientID not in consumerCache:
        pulsarSubscription = f'sub_{clientID}'
        consumerCache[clientID] = puClient.subscribe(
            'persistent://og1/default/t1',
            pulsarSubscription)
    #
    return consumerCache[clientID]


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
