"""
    api.py
    Run with:
        uvicorn api:app
"""

import asyncio
import json
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from pulsarTools import (getPulsarClient, getConsumer, getProducer,
                         receiveOrNone)
from utils import dictMerge
from messaging import (validatePosition, makeLeavingUpdate, makeGeometryUpdate,
                       makeWelcomeUpdate, makeEnteringPositionUpdate)
from gameStatus import (storeGamePlayerStatus, retrieveGamePlayerStatuses,
                        retrieveGamePlayerStatus, storeGameInactivePlayer)

from settings import (HALF_SIZE_X, HALF_SIZE_Y, RECEIVE_TIMEOUTS_MS,
                      SLEEP_BETWEEN_READS_MS)

app = FastAPI()
gameID = uuid4()

@app.websocket("/ws/world/{client_id}")
async def worldWSRoute(worldWS: WebSocket, client_id: str):
    await worldWS.accept()
    #
    pulsarClient = getPulsarClient()
    pulsarConsumer = getConsumer(client_id, pulsarClient)
    #
    try:
        # we start picking messages from the Pulsar 'bus'
        # and routing them to this client
        while True:
            worldUpdateMsg = receiveOrNone(pulsarConsumer, RECEIVE_TIMEOUTS_MS)
            if worldUpdateMsg is not None:
                # We forward any update from Pulsar into the 'world' websocket
                # for all clients out there:
                await worldWS.send_text(worldUpdateMsg.data().decode())
                pulsarConsumer.acknowledge(worldUpdateMsg)
            await asyncio.sleep(SLEEP_BETWEEN_READS_MS / 1000)
    except WebSocketDisconnect:
        pulsarConsumer.close()


@app.websocket("/ws/player/{client_id}")
async def playerWSRoute(playerWS: WebSocket, client_id: str):
    await playerWS.accept()
    #
    pulsarClient = getPulsarClient()
    pulsarProducer = getProducer(pulsarClient)
    #
    while True:
        try:
            # Any update from a player coming through the 'player' websocket
            updateMsgBlob = await playerWS.receive_text()
            updateMsg = json.loads(updateMsgBlob)
            if updateMsg['messageType'] == 'player':
                # if it is a player position update ...
                # ... is then validated, enriched ...
                playerUpdate = validatePosition(updateMsg, HALF_SIZE_X,
                                                HALF_SIZE_Y)
                #
                fullUpdate = dictMerge(playerUpdate, {'playerID': client_id})
                # ... persisted in the server-side status...
                storeGamePlayerStatus(gameID, fullUpdate)
                # ... and finally sent to Pulsar
                pulsarProducer.send((json.dumps(fullUpdate)).encode('utf-8'))
            elif updateMsg['messageType'] == 'leaving':
                # Player is leaving the game: we update our state to reflect this
                storeGameInactivePlayer(gameID, client_id)
                # ...but also broadcast this information to all players
                fullUpdate = dictMerge(updateMsg, {'playerID': client_id})
                pulsarProducer.send((json.dumps(fullUpdate)).encode('utf-8'))
            elif updateMsg['messageType'] == 'entering':
                # A new player announced they're entering and is asking for data
                # first we tell this client how the game-field looks like
                geomUpdate = makeGeometryUpdate(HALF_SIZE_X, HALF_SIZE_Y)
                # Note: this message is built here (i.e. no Pulsar involved)
                # and directly sent to a single client, the one who just connected:
                await playerWS.send_text(json.dumps(geomUpdate))
                # we brief the newcomer on all players on the stage
                for ops in retrieveGamePlayerStatuses(gameID, {client_id}):
                    await playerWS.send_text(json.dumps(ops))
                # do we have a previously-stored position/status for this same player?
                plStatus = retrieveGamePlayerStatus(gameID, client_id)
                if plStatus is not None:
                    await playerWS.send_text(json.dumps(plStatus))
                    # returning players: we want to route their return to pulsar as well
                    pulsarProducer.send((json.dumps(plStatus)).encode('utf-8'))
                else:
                    firstPos = makeEnteringPositionUpdate(
                        client_id=client_id,
                        client_name=updateMsg['payload']['name'],
                        halfX=HALF_SIZE_X,
                        halfY=HALF_SIZE_Y)
                    await playerWS.send_text(json.dumps(firstPos))
            else:
                # other types of message undergo no validation whatsoever:
                # we simply add the player ID to the message and publish
                fullUpdate = dictMerge(updateMsg, {'playerID': client_id})
                pulsarProducer.send((json.dumps(fullUpdate)).encode('utf-8'))
        except WebSocketDisconnect:
            # In this case we issue the "goodbye message" (i.e. null position)
            # on behalf of the client
            leavingUpdate = makeLeavingUpdate(client_id)
            # ... we store the disappearance of the player
            storeGameInactivePlayer(gameID, client_id)
            # ... and we send it to Pulsar for everyone:
            pulsarProducer.send((json.dumps(leavingUpdate)).encode('utf-8'))
