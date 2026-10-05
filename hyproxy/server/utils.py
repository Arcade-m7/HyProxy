from os import urandom

def randid():
    """
    Return a random hex identifier used as listener name.
    params:
        None
    returns:
        str : a random 12-character hex identifier
    errors:
        None
    """
    return urandom(6).hex().upper()
