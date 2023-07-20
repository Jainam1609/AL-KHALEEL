class TableAB:
    def __init__(self, prefix, stem):
        self.prefix = prefix
        self.stem = stem

    def __repr__(self):
        return "TableAB(prefix='{}', stem='{}')".format(self.prefix, self.stem)
