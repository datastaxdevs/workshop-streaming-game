"""
    dal.py
        In-memory access layer, alternative to an actual storage.

        Useful for quick debugging or to overcome less-than-ideal deployments,
        in particular those with the API far from the DB (e.g. Gitpod vs Astra DB).
        This helps relieve latency issues, at the price that the API would not
        be able to scale to more processes as the whole "persisted game state"
        remains process-local.

    Note: not particularly optimized (or elegant at that).
"""


# a map gameID -> kind -> objectID -> whole dict
memStorage = {}


def _ensureGameID(uGameID):
    memStorage[uGameID] = memStorage.get(uGameID, {})


def _ensureKind(uGameID, kind):
    _ensureGameID(uGameID)
    memStorage[uGameID][kind] = memStorage[uGameID].get(kind, {})


def _ensureObjectID(uGameID, kind, uObjectID):
    _ensureKind(uGameID, kind)
    memStorage[uGameID][kind][uObjectID] = memStorage[uGameID][kind].get(uObjectID, {})


def _qualify(gid, kdd, oid, rec, columns=None):
    # add the "primary key" to entries found in the mem storage
    r = {k: v for k, v in rec.items()}
    r['game_id'] = gid
    r['kind'] = kdd
    r['object_id'] = oid
    return {
        k: v
        for k, v in r.items()
        if columns is None or k in columns
    }


##


def storeActivity(uGameID, kind, uObjectID, active):
    _ensureObjectID(uGameID, kind, uObjectID)
    #
    memStorage[uGameID][kind][uObjectID]['active'] = active


def storeObject(uGameID, kind, uObjectID, active, x, y, h, generation, name):
    _ensureObjectID(uGameID, kind, uObjectID)
    #
    memStorage[uGameID][kind][uObjectID] = {
        'active': active,
        'x': x,
        'y': y,
        'h': h,
        'generation': generation,
        'name': name,
    }


def storeCoordinates(uGameID, kind, uObjectID, active, x, y):
    _ensureObjectID(uGameID, kind, uObjectID)
    #
    memStorage[uGameID][kind][uObjectID]['x'] = x
    memStorage[uGameID][kind][uObjectID]['y'] = y
    memStorage[uGameID][kind][uObjectID]['active'] = active


def retrieveByGameID(uGameID):
    _ensureGameID(uGameID)
    #
    return (
        _qualify(
            uGameID,
            kd,
            oID,
            record,
            {'kind', 'object_id', 'active', 'x', 'y', 'h', 'generation', 'name'},
        )
        for kd, oidmap in memStorage[uGameID].items()
        for oID, record in oidmap.items()
    )


def retrieveShortByGameID(uGameID):
    _ensureGameID(uGameID)
    #
    return (
        _qualify(
            uGameID,
            kd,
            oID,
            record,
            {'kind', 'object_id', 'active', 'x', 'y', 'name'},
        )
        for kd, oidmap in memStorage[uGameID].items()
        for oID, record in oidmap.items()
    )


def retrieveObjectByID(uGameID, kind, uObjectID):
    _ensureKind(uGameID, kind)
    #
    if uObjectID in memStorage[uGameID][kind]:
        return _qualify(
            uGameID,
            kind,
            uObjectID,
            memStorage[uGameID][kind][uObjectID],
            {'object_id', 'x', 'y', 'h', 'generation', 'name'},
        )
    else:
        return None


def retrieveOneShortByKind(uGameID, kind):
    _ensureKind(uGameID, kind)
    #
    found = [
        _qualify(
            uGameID,
            kind,
            oID,
            record,
            {'object_id', 'active', 'x', 'y'},
        )
        for oID, record in memStorage[uGameID][kind].items()
    ]
    if found == []:
        return None
    else:
        return found[0]
