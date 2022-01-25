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

from messaging import (makePositionUpdate, pickBrickPositions, makeBrickUpdate)
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
psSelectObjectCQL = session.prepare(
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
    'SELECT kind, object_id, active, x, y FROM '
    'objects_by_game_id WHERE game_id = ?;'
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


def _dbRowToMessage(row):
    if row.kind == 'player':
        return _dbRowToPlayerMessage(row)
    elif row.kind == 'brick':
        return _dbRowToBrickMessage(row)

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
        psSelectObjectCQL,
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
    # TODO read for bricks
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
