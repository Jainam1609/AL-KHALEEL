class TableBC:
    def __init__(self, stem, suffix):
        self.stem = stem
        self.suffix = suffix

    def __repr__(self):
        return "TableBC(stem='{}', suffix='{}')".format(self.stem, self.suffix)
