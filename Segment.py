class Segment:
    def __init__(self, newPrefix, newStem, newSuffix):
        self.prefix = newPrefix
        self.stem = newStem
        self.suffix = newSuffix

    @property
    def Prefix(self):
        return self.prefix

    @Prefix.setter
    def Prefix(self, value):
        self.prefix = value

    @property
    def Stem(self):
        return self.stem

    @Stem.setter
    def Stem(self, value):
        self.stem = value

    @property
    def Suffix(self):
        return self.suffix

    @Suffix.setter
    def Suffix(self, value):
        self.suffix = value
