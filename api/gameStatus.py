"""
    gameStatus.py
        A persistence layer for the game.
        For simplicity, player-info entering and exiting this library
        are directly in the form of "player" messages. A bit of a tight
        coupling, but for illustration purposes it keeps everything simpler
        (one may want to more clearly decouple the two representations,
        row and 'player' message, in a more structured application).
"""

import uuid

from messaging import (makePositionUpdate, pickBrickPositions, makeBrickUpdate,
                       pickFoodPositions, makeFoodUpdate)
from database.session import session


# prepared statements are created here for later usage:
psInsertObjectCQL = session.prepare(
    'INSERT INTO objects_by_game_id (game_id, kind, object_id, active, '
    'x, y, h, generation, name) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? );'
)
psInsertObjectCoordinatesCQL = session.prepare(
    'INSERT INTO objects_by_game_id (game_id, kind, object_id, '
    'x, y) VALUES ( ?, ?, ?, ?, ? );'
)
psSelectObjectByIDCQL = session.prepare(
    'SELECT object_id, x, y, h, generation, name FROM objects_by_game_id WHERE '
    'game_id = ? AND kind = ? AND object_id = ?'
)
psSelectObjectsCQL = session.prepare(
    'SELECT kind, object_id, active, x, y, h, generation, name FROM '
    'objects_by_game_id WHERE game_id = ?;'
)
psInsertObjectActivenessCQL = session.prepare(
    'INSERT INTO objects_by_game_id (game_id, kind, object_id, active) VALUES '
    '(?, ?, ?, ?);'
)
psSelectObjectsShortCQL = session.prepare(
    'SELECT kind, object_id, active, x, y, name FROM '
    'objects_by_game_id WHERE game_id = ?;'
)
psSelectObjectsShortByKindCQL = session.prepare(
    'SELECT object_id, active, x, y FROM '
    'objects_by_game_id WHERE game_id = ? AND kind = ?;'
)

def _dbRowToPlayerMessage(row):
    # args are: client_id, client_name, x, y, h, generation
    return makePositionUpdate(
        str(row.object_id),
        row.name,
        row.x,
        row.y,
        row.h,
        row.generation,
    )


def _dbRowToBrickMessage(row):
    return makeBrickUpdate(
        row.name,
        row.x,
        row.y,
    )


def _dbRowToFoodMessage(row):
    return makeFoodUpdate(
        row.object_id,
        row.name,
        row.x,
        row.y,
    )


def _dbRowToMessage(row):
    if row.kind == 'player':
        return _dbRowToPlayerMessage(row)
    elif row.kind == 'brick':
        return _dbRowToBrickMessage(row)
    elif row.kind == 'food':
        return _dbRowToFoodMessage(row)
    else:
        raise NotImplementedError('Unknown row kind "%s"' % row.kind)

###


def _storeGameActivityForPlayer(gameID, playerID, active):
    session.execute(
        psInsertObjectActivenessCQL,
        (
            uuid.UUID(gameID),
            'player',
            uuid.UUID(playerID),
            active,
        ),
    )


def storeGameActivePlayer(gameID, playerID):
    """
        Side-effect only: marking a player as 'active (again) on board'
        (i.e. when coming back to same game).
    """
    _storeGameActivityForPlayer(gameID, playerID, True)


def storeGameInactivePlayer(gameID, playerID):
    """
        Side-effect only: marking a player as 'inactive from board'
        (i.e. when disconnecting from game).
    """
    _storeGameActivityForPlayer(gameID, playerID, False)


def storeFoodItemStatus(gameID, foodUpdate):
    """
        Side-effect only: stores the last location/status of
        a food item on the field.

        Input is a 'food' message, parsed here internally
    """
    #
    pLoad = foodUpdate['payload']
    foodID = foodUpdate['foodID']
    session.execute(
        psInsertObjectCQL,
        (
            uuid.UUID(gameID),
            'food',
            uuid.UUID(foodID),
            True,
            pLoad['x'],
            pLoad['y'],
            False,
            0,
            pLoad['name'],
        ),
    )



def storeGamePlayerStatus(gameID, playerUpdate):
    """
        Side-effect only: stores the last location/status of
        a player on the field.

        Input is a 'player' message, parsed here internally
    """
    #
    pLoad = playerUpdate['payload']
    playerID = playerUpdate['playerID']
    session.execute(
        psInsertObjectCQL,
        (
            uuid.UUID(gameID),
            'player',
            uuid.UUID(playerID),
            True,
            pLoad['x'],
            pLoad['y'],
            pLoad['h'],
            pLoad['generation'],
            pLoad['name'],
        ),
    )


def storeGamePlayerPosition(gameID, playerID, x, y):
    """
        Store new coordinates (server-forced), for later validation etc.
    """
    session.execute(
        psInsertObjectCoordinatesCQL,
        (
            uuid.UUID(gameID),
            'player',
            uuid.UUID(playerID),
            x,
            y,
        ),
    )


def retrieveActiveGameItems(gameID, excludedPlayerIDs = set()):
    """
        Return active players only. Output are 'player' messages ready-to-send.
    """
    results = session.execute(
        psSelectObjectsCQL,
        (uuid.UUID(gameID), ),
    )
    return (
        _dbRowToMessage(row)
        for row in results
        if row.active
        if row.kind != 'player' or str(row.object_id) not in excludedPlayerIDs
    )


def retrieveFieldOccupancy(gameID):
    """
        Return a map (x, y) -> {kind: ... , object_id: ...}, skips inactives
    """
    results = session.execute(
        psSelectObjectsShortCQL,
        (uuid.UUID(gameID), ),
    )
    return {
        (row.x, row.y): {
            'kind': row.kind,
            'object_id': row.object_id,
            'name': row.name,
        }
        for row in results
        if row.active
    }


def retrieveGamePlayerStatus(gameID, playerID):
    """
        Return None if no info found,
        else a 'player' message (which, as such, knows of no 'active' flag).
    """
    result = session.execute(
        psSelectObjectByIDCQL,
        (
            uuid.UUID(gameID),
            'player',
            uuid.UUID(playerID),
        ),
    ).one()
    if result is None:
        return None
    else:
        return _dbRowToPlayerMessage(result)


def layBricks(gameID, HALF_SIZE_X, HALF_SIZE_Y, BRICK_FRACTION):
    """
        this creates the bricks for the game.
        It should run only once per gameID (hence we perform a read and make
        sure there are no bricks), but before any player joins.
    """

    # first check if there are bricks already (even just one)
    prevBrick = session.execute(
        psSelectObjectsShortByKindCQL,
        (
            uuid.UUID(gameID),
            'brick',
        ),
    ).one()
    if prevBrick is not None:
        # bricks already present
        return
    else:
        # we create the required bricks
        brickPositions = pickBrickPositions(
            2*HALF_SIZE_X-1,
            2*HALF_SIZE_Y-1,
            BRICK_FRACTION,
        )
        # we store the bricks for this game
        _gameID = uuid.UUID(gameID)
        for bi, (bx, by) in enumerate(brickPositions):
            session.execute(
                psInsertObjectCQL,
                (
                    _gameID,
                    'brick',
                    uuid.uuid4(),
                    True,
                    bx,
                    by,
                    False,
                    0,
                    'brick_%04i' % bi,
                ),
            )

def layFood(gameID, HALF_SIZE_X, HALF_SIZE_Y, NUM_FOOD_ITEMS):
    """
        we read the gamefield and place an exact number of food
        items on the board, unless there are already some.
    """
    # first check if there are food items already (even just one)
    prevFood = session.execute(
        psSelectObjectsShortByKindCQL,
        (
            uuid.UUID(gameID),
            'food',
        ),
    ).one()
    if prevFood is not None:
        # food already present
        return
    else:
        # we survey forbidden locations first
        occupancyMap = retrieveFieldOccupancy(gameID)
        # we create the required food
        foodPositions = pickFoodPositions(
            2*HALF_SIZE_X-1,
            2*HALF_SIZE_Y-1,
            NUM_FOOD_ITEMS,
            occupancyMap,
        )
        # we store the bricks for this game
        _gameID = uuid.UUID(gameID)
        for fi, (fx, fy) in enumerate(foodPositions):
            session.execute(
                psInsertObjectCQL,
                (
                    _gameID,
                    'food',
                    uuid.uuid4(),
                    True,
                    fx,
                    fy,
                    False,
                    0,
                    'food_%04i' % fi,
                ),
            )
