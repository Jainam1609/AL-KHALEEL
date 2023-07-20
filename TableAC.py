class TableAC:
    def __init__(self, prefix, suffix):
        self.prefix = prefix
        self.suffix = suffix

    def __repr__(self):
        return "TableAC(prefix='{}', suffix='{}')".format(self.prefix, self.suffix)
