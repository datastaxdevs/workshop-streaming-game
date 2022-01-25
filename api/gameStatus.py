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
psInsertPlayerByPlayerID = session.prepare(
    'INSERT INTO players_by_player_id (game_id, player_id, active, '
    'x, y, h, generation, name) VALUES ( ?, ?, ?, ?, ?, ?, ?, ? );'
)
psSelectPlayerByPlayerID = session.prepare(
    'SELECT player_id, x, y, h, generation, name FROM players_by_player_id WHERE '
    'game_id = ? AND player_id = ?'
)
psSelectPlayersByPlayerID = session.prepare(
    'SELECT player_id, active, x, y, h, generation, name FROM '
    'players_by_player_id WHERE game_id = ?;'
)
psInsertInactivePlayerByPlayerID = session.prepare(
    'INSERT INTO players_by_player_id (game_id, player_id, active) VALUES '
    '(?, ?, ?);'
)


def _dbRowToPlayerMessage(row):
    # args are: client_id, client_name, x, y, h, generation
    print('CONVERTING %s' % row.name)
    return makePositionUpdate(
        str(row.player_id),
        row.name,
        row.x,
        row.y,
        row.h,
        row.generation,
    )


###

def storeGameInactivePlayer(gameID, playerID):
    """
        Side-effect only: marking a player as 'inactive from board'
        (i.e. when disconnecting from game).
    """
    session.execute(
        psInsertInactivePlayerByPlayerID,
        (
            uuid.UUID(gameID),
            uuid.UUID(playerID),
            False,
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
        psInsertPlayerByPlayerID,
        (
            uuid.UUID(gameID),
            uuid.UUID(playerID),
            True,
            pLoad['x'],
            pLoad['y'],
            pLoad['h'],
            pLoad['generation'],
            pLoad['name'],
        ),
    )


def retrieveActiveGamePlayerStatuses(gameID, excludedIDs = set()):
    """
        Return active players only. Output are 'player' messages ready-to-send.
    """
    results = session.execute(
        psSelectPlayersByPlayerID,
        (uuid.UUID(gameID), ),
    )
    return (
        _dbRowToPlayerMessage(row)
        for row in results
        if row.active
        if str(row.player_id) not in excludedIDs
    )


def retrieveGamePlayerStatus(gameID, playerID):
    """
        Return None if no info found,
        else a 'player' message (which, as such, knows of no 'active' flag).
    """
    result = session.execute(
        psSelectPlayerByPlayerID,
        (
            uuid.UUID(gameID),
            uuid.UUID(playerID),
        ),
    ).one()
    if result is None:
        return None
    else:
        return _dbRowToPlayerMessage(result)
