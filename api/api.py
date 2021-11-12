"""
    api.py
    Run with:
        source ../.env
        uvicorn api:app --reload
"""

import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from pulsarTools import (getPulsarClient, getConsumer, getProducer,
                         receiveOrNone)
from utils import dictMerge
from messaging import (validatePosition, makeGoodbyeUpdate, makeGeometryUpdate,
                       makeWelcomeUpdate)

from settings import (HALF_SIZE_X, HALF_SIZE_Y, RECEIVE_TIMEOUTS_MS,
                      SLEEP_BETWEEN_READS_MS)

app = FastAPI()


@app.websocket("/ws/world/{client_id}")
async def worldWSRoute(worldWS: WebSocket, client_id: str):
    await worldWS.accept()
    #
    pulsarClient = getPulsarClient()
    pulsarConsumer = getConsumer(client_id, pulsarClient)
    #
    try:
        # first we tell this client how the game-field looks like
        geomUpdate = makeGeometryUpdate(HALF_SIZE_X, HALF_SIZE_Y)
        # Note: this message is built here (i.e. no Pulsar involved)
        # and directly sent to a single client, the one who just connected:
        await worldWS.send_text(json.dumps(geomUpdate))
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
                fullUpdate = dictMerge(playerUpdate, {'playerID': client_id})
                # ... and finally sent to Pulsar
                pulsarProducer.send((json.dumps(fullUpdate)).encode('utf-8'))
            else:
                # other types of message undergo no validation whatsoever:
                # we simply add the player ID to the message and publish
                fullUpdate = dictMerge(updateMsg, {'playerID': client_id})
                pulsarProducer.send((json.dumps(fullUpdate)).encode('utf-8'))
        except WebSocketDisconnect:
            # In this case we issue the "goodbye message" (i.e. null position)
            # on behalf of the client, and we send it to Pulsar for everyone:
            goodbyeUpdate = makeGoodbyeUpdate(client_id)
            pulsarProducer.send((json.dumps(goodbyeUpdate)).encode('utf-8'))
