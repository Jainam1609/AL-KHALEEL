class Dictionary:
    def __init__(self, e=None, v=None, c=None, g=None, p=None, obj=None):
        if obj is not None:
            self.entry = obj.entry
            self.voc = obj.voc
            self.cat = obj.cat
            self.gloss = obj.gloss
            self.pos = obj.pos
        else:
            self.entry = e
            self.voc = v
            self.cat = c
            self.gloss = g
            self.pos = p

    # def __init__(self, obj):
    #     self.entry = obj.entry
    #     self.voc = obj.voc
    #     self.cat = obj.cat
    #     self.gloss = obj.gloss
    #     self.pos = obj.pos

    @property
    def Entry(self):
        return self.entry

    @Entry.setter
    def Entry(self, value):
        self.entry = value

    @property
    def Voc(self):
        return self.voc

    @Voc.setter
    def Voc(self, value):
        self.voc = value

    @property
    def Cat(self):
        return self.cat

    @Cat.setter
    def Cat(self, value):
        self.cat = value

    @property
    def Gloss(self):
        return self.gloss

    @Gloss.setter
    def Gloss(self, value):
        self.gloss = value

    @property
    def POS(self):
        return self.pos

    @POS.setter
    def POS(self, value):
        self.pos = value

    def __str__(self):
        return "Entry = " + self.Entry + "  Voc = " + self.Voc + "  Cat = " + self.Cat + "  Gloss = " + self.Gloss + "  POS = " + self.POS
