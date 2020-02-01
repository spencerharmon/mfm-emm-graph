class Atom(object):
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.name = data["name"]
        self.argb = data["argb"]
        self.data_members = data["data_members"]

    def __repr__(self):
        return self.symbol.ljust(2, ' ')


class Empty(Atom):
    """
    Special atom type. Usefull for type hinting
    """
    def __init__(self, data={"name": "Empty"}):
        self.symbol = "__"
        self.name = "Empty"
        self.argb = "FFF"
        self.data_members = {}


class Identifier(Atom):
    """
    Special atom type. Useful for type hinting
    """
    pass
