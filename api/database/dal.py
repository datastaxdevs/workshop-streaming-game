"""
    dal.py
        Cassandra (or Astra DB) access layer
"""

from .dbsession import session


# prepared statements are created here for later usage:
psInsertObjectCQL = session.prepare(
    'INSERT INTO objects_by_game_id (game_id, kind, object_id, active, '
    'x, y, h, generation, name) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? );'
)
psInsertObjectCoordinatesCQL = session.prepare(
    'INSERT INTO objects_by_game_id (game_id, kind, object_id, '
    'active, x, y) VALUES ( ?, ?, ?, ?, ?, ? );'
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

##


def storeActivity(uGameID, kind, uObjectID, active):
    session.execute(
        psInsertObjectActivenessCQL,
        (
            uGameID, kind, uObjectID, active,
        ),
    )


def storeObject(uGameID, kind, uObjectID, active, x, y, h, generation, name):
    session.execute(
    psInsertObjectCQL,
    (
        uGameID, kind, uObjectID, active, x, y, h, generation, name,
    ),
)


def storeCoordinates(uGameID, kind, uObjectID, active, x, y):
    session.execute(
        psInsertObjectCoordinatesCQL,
        (
            uGameID, kind, uObjectID, active, x, y,
        ),
    )


def retrieveByGameID(uGameID):
    results = session.execute(
        psSelectObjectsCQL,
        (uGameID, ),
    )
    return (
        row._asdict()
        for row in results
    )



def retrieveShortByGameID(uGameID):
    results = session.execute(
        psSelectObjectsShortCQL,
        (uGameID, ),
    )
    return (
        row._asdict()
        for row in results
    )


def retrieveObjectByID(uGameID, kind, uObjectID):
    result = session.execute(
        psSelectObjectByIDCQL,
        (
            uGameID, kind, uObjectID,
        ),
    ).one()
    if result is None:
        return None
    else:
        return result._asdict()


def retrieveOneShortByKind(uGameID, kind):
    item = session.execute(
        psSelectObjectsShortByKindCQL,
        (
            uGameID, kind,
        ),
    ).one()
    if item is not None:
        return item._asdict()
    else:
        return None
