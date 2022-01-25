"""
    messaging.py
"""

import time
import random
from uuid import uuid4

from utils import dictMerge


# poor randomness, not a problem here
random.seed(int(time.time()))


def makeCoordPair(updDict):
    if updDict is None:
        return (None, None)
    else:
        return (
            updDict['payload']['x'],
            updDict['payload']['y'],
        )


def validatePosition(updDict, halfX, halfY, fieldOccupancy, prevUpdate):
    """
    Utility function to keep the 'x' and 'y' in a dict
    bound within the game field,
    respecting other keys in the passed dict.
    """
    def _constrain(val, minv, maxv):
        return max(minv, min(val, maxv))

    # update wants to get to these coordinates:
    updX = updDict['payload']['x']
    updY = updDict['payload']['y']
    # None values are a init transient, we ignore validation

    if updX is None or updY is None:
        # "everything goes"
        return updDict
    else:
        cnewX = _constrain(updX, 0, 2*halfX - 2)
        cnewY = _constrain(updY, 0, 2*halfY - 2)
        # can player get to that position?
        targetIsFree = (cnewX, cnewY) not in fieldOccupancy
        #
        if prevUpdate is None:
            curX = halfX - 1
            curY = halfY - 1
        else:
            curX = prevUpdate['payload']['x']
            curY = prevUpdate['payload']['y']
        if curX is not None and curY is not None:
            targetIsNear = abs(curX - cnewX) < 2 and abs(curY - cnewY) < 2
        else:
            targetIsNear = True
        #
        canGetThere = targetIsFree and targetIsNear
        if canGetThere:
            # yes, it can
            newPosPayload = {
                'x': cnewX,
                'y': cnewY,
            }
            return dictMerge(
                {
                    'payload': newPosPayload,
                },
                default=updDict,
            )
        else:
            cbX = curX
            cbY = curY
            newPosPayload = {
                'x': cbX,
                'y': cbY,
            }
            return dictMerge(
                {
                    'payload': newPosPayload,
                },
                default=updDict,
            )


def makePositionUpdate(client_id, client_name, x, y, h, generation):
    return {
        'messageType': 'player',
        'playerID': client_id,
        'payload': {
            'x': x,
            'y': y,
            'h': h,
            'generation': generation,
            'name': client_name,
        },
    }    


def makeEnteringPositionUpdate(client_id, client_name, halfX, halfY,
                               occupancyMap):
    # we randomize and take care to avoid cells with anything in them
    freeCells = [
        (x, y)
        for x in range(2*halfX - 1)
        for y in range(2*halfY - 1)
        if (x, y) not in occupancyMap
    ]
    if len(freeCells) > 0:
        tX, tY = freeCells[random.randint(0, len(freeCells)-1)]
    else:
        tX = halfX - 1
        tY = halfY - 1
    #
    return makePositionUpdate(client_id, client_name, tX, tY,
                              False, 0)


def makeLeavingUpdate(client_id):
    """
    A default 'leaving' message to publish to the Pulsar topic
    in case a client disconnection is detected
    """
    return {
        'messageType': 'leaving',
        'playerID': client_id,
        'payload': {
            'name': '',
        },
    }


def makeWelcomeUpdate(client_id):
    """
    A server-generated chat message to greet a new player
    """
    return {
        'messageType': 'chat',
        'payload': {
            'id': str(uuid4()),
            'name': '** API **',
            'text': 'Welcome to the game!',
        },
        'playerID': '_api_server_',
    }


def makeGeometryUpdate(hsX, hsY):
    """
    Prepare a message containing the field geometry info
    """
    return {
        'messageType': 'geometry',
        'payload': {
            'halfSizeX': hsX,
            'halfSizeY': hsY,
        },
    }
