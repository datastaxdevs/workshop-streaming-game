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

from messaging import makePositionUpdate
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
psSelectObjectsByKindCQL = session.prepare(
    'SELECT object_id, active, x, y, h, generation, name FROM '
    'objects_by_game_id WHERE game_id = ? AND kind = ?;'
)
psInsertObjectActivenessCQL = session.prepare(
    'INSERT INTO objects_by_game_id (game_id, kind, object_id, active) VALUES '
    '(?, ?, ?, ?);'
)
psSelectObjectsCQL = session.prepare(
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


def retrieveActiveGamePlayerStatuses(gameID, excludedIDs = set()):
    """
        Return active players only. Output are 'player' messages ready-to-send.
    """
    results = session.execute(
        psSelectObjectsByKindCQL,
        (uuid.UUID(gameID), 'player' ),
    )
    return (
        _dbRowToPlayerMessage(row)
        for row in results
        if row.active
        if str(row.object_id) not in excludedIDs
    )


def retrieveFieldOccupancy(gameID):
    """
        Return a map (x, y) -> {kind: ... , object_id: ...}, skips inactives
    """
    results = session.execute(
        psSelectObjectsCQL,
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
