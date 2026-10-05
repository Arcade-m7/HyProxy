class Protocols(dict):

    def __init__(self, iterable):
        super().__init__(iterable)
        """
        Initialize protocol mapping dictionary.
        params:
            iterable : iterable : initial data for the dict
        returns:
            None
        errors:
            Exception : if iterable cannot initialize the dict
        """

    @classmethod
    def add(cls, li: list):
        """
        Return a list of (name, protocol) pairs to register supported protocols.
        params:
            li : list : list of protocol classes
        returns:
            list[tuple[str,Any]] : list of (name, protocol) pairs
        errors:
            AssertionError : if `li` is not a list
        """
        assert isinstance(li, list)
        return cls([
            (str(pr),pr) for pr in li
        ])