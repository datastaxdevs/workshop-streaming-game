"""
    utils.py
"""


def dictMerge(main, default):
    """
    Pure dict deep-merge function. First dict has precedence.
    """
    if isinstance(main, dict):
        return {
            k: dictMerge(
                main[k],
                default=({} if default is None else default).get(k),
            ) if k in main else default[k]
            for k in ({} if default is None else default.keys()) | main.keys()
        }
    else:
        return main


def validatePosition(updDict, halfX, halfY):
    """
    Utility function to keep the 'x' and 'y' in a dict
    bound within the game field, respecting null values and other keys
    that may be present in the dict expressing the item position.
    """
    def _constrainNoneAware(val, minv, maxv):
        if val is None:
            return val
        else:
            return max(minv, min(val, maxv))

    payload = {
        'x': _constrainNoneAware(updDict['payload']['x'], 0, 2*halfX - 2),
        'y': _constrainNoneAware(updDict['payload']['y'], 0, 2*halfY - 2),
    }
    return dictMerge(
        {
            'payload': payload,
        },
        default=updDict,
    )
