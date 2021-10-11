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

from pulsarTools import getPulsarClient, getConsumer, receiveOrNone
from utils import dictMerge, validatePosition

from settings import (HALF_SIZE_X, HALF_SIZE_Y, RECEIVE_TIMEOUTS_MS,
                      SLEEP_BETWEEN_READS_MS)

app = FastAPI()


@app.websocket("/ws/world/{client_id}")
async def worldWSRoute(worldWS: WebSocket, client_id: str):
    await worldWS.accept()
    #
    pulsarClient = getPulsarClient()
    pulsarConsumer = getConsumer(client_id, pulsarClient)
    # pulsarSubscription = f'sub_{client_id}'
    # pulsarConsumer = pulsarClient.subscribe('persistent://og1/default/t1',
                                            # pulsarSubscription)
    #
    pulsarProducer = pulsarClient.create_producer(
        'persistent://og1/default/t1'
    )
    pulsarProducer.close()
    #
    try:
        while True:
            worldUpdateMsg = receiveOrNone(pulsarConsumer, RECEIVE_TIMEOUTS_MS)
            if worldUpdateMsg is not None:
                # We forward any update from Pulsar into the 'world' websocket
                # for all clients out there:
                await worldWS.send_text(worldUpdateMsg.data().decode())
            await asyncio.sleep(SLEEP_BETWEEN_READS_MS / 1000)
    except WebSocketDisconnect:
        pulsarConsumer.close()


@app.websocket("/ws/player/{client_id}")
async def playerWSRoute(playerWS: WebSocket, client_id: str):
    await playerWS.accept()
    #
    pulsarClient = getPulsarClient()
    pulsarProducer = pulsarClient.create_producer(
        'persistent://og1/default/t1'
    )
    #
    while True:
        try:
            # Any update from a player coming through the 'player' websocket
            playerUpdateMsg = await playerWS.receive_text()
            playerUpdateReq = json.loads(playerUpdateMsg)
            # ... is then validated, enriched ...
            playerUpdate = validatePosition(playerUpdateReq, HALF_SIZE_X,
                                            HALF_SIZE_Y)
            fullUpdate = dictMerge(playerUpdate, {'playerID': client_id})
            # ... and finally sent to Pulsar
            pulsarProducer.send((json.dumps(fullUpdate)).encode('utf-8'))
        except WebSocketDisconnect:
            # In this case we issue the "goodbye message" (i.e. null position)
            # on behalf of the client, and we send it to Pulsar for everyone:
            fullUpdate = {
                'playerName': '',
                'playerID': client_id,
                'x': None,
                'y': None,
            }
            pulsarProducer.send((json.dumps(fullUpdate)).encode('utf-8'))
            return
