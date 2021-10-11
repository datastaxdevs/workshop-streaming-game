"""
    utils.py
"""


def dictMerge(main, default):
    """
    Pure dict deep-merge function. First dict has precedence.
    """
    if isinstance(main, dict):
        return {
            k: deep_merge(
                main[k],
                default=({} if default is None else default).get(k),
            ) if k in main else default[k]
            for k in ({} if default is None else default.keys()) | main.keys()
        }
    else:
        return main


def validatePosition(posDict, halfX, halfY):
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

    return deep_merge(
        {
            'x': _constrainNoneAware(posDict['x'], 0, 2*halfX - 2),
            'y': _constrainNoneAware(posDict['y'], 0, 2*halfY - 2),
        },
        default=posDict,
    )
