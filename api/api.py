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
                       makeWelcomeUpdate, makeEnteringPositionUpdate,
                       makeCoordPair, pickFoodPositions, makeFoodUpdate,
                       makeServerChatUpdate)
from gameStatus import (storeGamePlayerStatus, retrieveActiveGameItems,
                        retrieveGamePlayerStatus, storeGameInactivePlayer,
                        storeGameActivePlayer, retrieveFieldOccupancy,
                        storeGamePlayerPosition, storeFoodItemStatus,
                        layBricks, layFood)

from settings import (HALF_SIZE_X, HALF_SIZE_Y, RECEIVE_TIMEOUTS_MS,
                      SLEEP_BETWEEN_READS_MS, BRICK_FRACTION, NUM_FOOD_ITEMS)

app = FastAPI()
gameID = str(uuid4())


# a one-off gamefield initialization routine
layBricks(gameID, HALF_SIZE_X, HALF_SIZE_Y, BRICK_FRACTION)
layFood(gameID, HALF_SIZE_X, HALF_SIZE_Y, NUM_FOOD_ITEMS)

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
            # we unpack and inject playerID to the incoming message
            updateMsg = dictMerge(
                json.loads(updateMsgBlob),
                {'playerID': client_id},
            )
            if updateMsg['messageType'] == 'player':
                # if it's a player position update, retrieve gamefield status...
                fieldOccupancy = retrieveFieldOccupancy(gameID)
                # ... and last position for this player (if any)
                prevUpdate = retrieveGamePlayerStatus(gameID, client_id)
                # ... update is then validated ...
                playerUpdate, caughtFoodItem = validatePosition(
                    updateMsg,
                    HALF_SIZE_X,
                    HALF_SIZE_Y,
                    fieldOccupancy,
                    prevUpdate
                )
                # We deal with caught food, if any
                if caughtFoodItem is not None:
                    caughtFoodID = caughtFoodItem['object_id']
                    caughtFoodName = caughtFoodItem['name']
                    # relocate the food item
                    newFPos = list(pickFoodPositions(
                        2*HALF_SIZE_X-1,
                        2*HALF_SIZE_Y-1,
                        1,
                        fieldOccupancy,
                    ))[0]
                    # create the food update
                    foodUpdate = makeFoodUpdate(
                        caughtFoodID,
                        caughtFoodName,
                        newFPos[0],
                        newFPos[1],
                    )
                    # persist new location to DB
                    storeFoodItemStatus(gameID, foodUpdate)
                    # congratulate catcher
                    congratMessage = makeServerChatUpdate(client_id, 'Good catch!')
                    await playerWS.send_text(json.dumps(congratMessage))
                    # broadcast (to pulsar) new food update
                    pulsarProducer.send((json.dumps(foodUpdate)).encode('utf-8'))
                #
                # ... persisted in the server-side status...
                storeGamePlayerStatus(gameID, playerUpdate)
                # ... and finally sent to Pulsar
                pulsarProducer.send((json.dumps(playerUpdate)).encode('utf-8'))
            elif updateMsg['messageType'] == 'leaving':
                # Player is leaving the game: we update our state to reflect this
                storeGameInactivePlayer(gameID, client_id)
                # ...but also broadcast this information to all players
                pulsarProducer.send((json.dumps(updateMsg)).encode('utf-8'))
            elif updateMsg['messageType'] == 'entering':
                # A new player announced they're entering and is asking for data
                newPlayerName = updateMsg['payload']['name']
                # first we tell this client how the game-field looks like
                geomUpdate = makeGeometryUpdate(HALF_SIZE_X, HALF_SIZE_Y)
                # Note: this message is built here (i.e. no Pulsar involved)
                # and directly sent to a single client, the one who just connected:
                await playerWS.send_text(json.dumps(geomUpdate))
                # we brief the newcomer on all players on the stage
                for ops in retrieveActiveGameItems(gameID, {client_id}):
                    await playerWS.send_text(json.dumps(ops))
                # do we have a previously-stored position/status for this same player?
                plStatus = retrieveGamePlayerStatus(gameID, client_id)
                # we check the field occupancy for next step ...
                fieldOccupancy = retrieveFieldOccupancy(gameID)
                playerPrevCoords = makeCoordPair(plStatus)
                if plStatus is not None and playerPrevCoords not in fieldOccupancy:
                    renamedPlStatus = dictMerge(
                        {'payload': {'name': newPlayerName}},
                        plStatus,
                    )
                    await playerWS.send_text(json.dumps(renamedPlStatus))
                    # returning players: we want to route their return to pulsar as well
                    pulsarProducer.send((json.dumps(renamedPlStatus)).encode('utf-8'))
                    # and we also want to mark them as active
                    storeGameActivePlayer(gameID, client_id)
                else:
                    firstPos = makeEnteringPositionUpdate(
                        client_id=client_id,
                        client_name=newPlayerName,
                        halfX=HALF_SIZE_X,
                        halfY=HALF_SIZE_Y,
                        occupancyMap=fieldOccupancy,
                    )
                    await playerWS.send_text(json.dumps(firstPos))
                    storeGamePlayerPosition(gameID, client_id, True, *makeCoordPair(firstPos))
            else:
                # other types of message undergo no validation whatsoever:
                # we simply add the player ID to the message and publish
                pulsarProducer.send((json.dumps(updateMsg)).encode('utf-8'))
        except WebSocketDisconnect:
            # In this case we issue the "goodbye message" (i.e. null position)
            # on behalf of the client
            leavingUpdate = makeLeavingUpdate(client_id)
            # ... we store the disappearance of the player
            storeGameInactivePlayer(gameID, client_id)
            # ... and we send it to Pulsar for everyone:
            pulsarProducer.send((json.dumps(leavingUpdate)).encode('utf-8'))
