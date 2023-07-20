import codecs


class DicTable:
    dictStems = []
    dictSuffixes = []
    dictPrefixes = []
    tableAB = []
    tableBC = []
    tableAC = []

    def __init__(self):
        # self.Parent = parent
        self.lineNo = 0

    def loadTableAB(self):
        self.lineNo = 0
        with codecs.open("Doc\\tableAB.txt", encoding='utf-8') as ois:
            for line in ois:
                sb = self.lineParser(line)
                if len(sb) > 0:
                    self.dataParser(sb, self.tableAB, 0)
                self.lineNo += 1

    def loadTableBC(self):
        self.lineNo = 0
        with codecs.open("Doc\\tableBC.txt", encoding='utf-8') as ois:
            for line in ois:
                sb = self.lineParser(line)
                if len(sb) > 0:
                    self.dataParser(sb, self.tableBC, 1)
                self.lineNo += 1

    def loadTableAC(self):
        self.lineNo = 0
        with codecs.open("Doc\\tableAC.txt", encoding='utf-8') as ois:
            for line in ois:
                sb = self.lineParser(line)
                if len(sb) > 0:
                    self.dataParser(sb, self.tableAC, 2)
                self.lineNo += 1

    def loadDictionaries(self):
        # self.Parent = parent
        self.loadTableAB()
        self.loadTableBC()
        self.loadTableAC()
        self.loadDictionary("Doc\\dictPrefixes.txt", self.dictPrefixes)
        self.loadDictionary("Doc\\dictSuffixes.txt", self.dictSuffixes)
        self.loadDictionary("Doc\\dictStems.txt", self.dictStems)

    def loadDictionary(self, fileName, dict):
        self.lineNo = 0
        with codecs.open(fileName, encoding='utf-8') as ois:
            for line in ois:
                sb = self.lineParser(line)
                if len(sb) > 0:
                    self.dicParser(sb, dict)
                self.lineNo += 1

    def lineParser(self, line):
        str = ""
        if len(line) > 0 and line[0] == ';':
            if len(line) > 1 and line[1] == ';':
                str = line
        else:
            str = line
        return str.strip()

    def dataParser(self, line, dict, table):
        Entry1 = ""
        Entry2 = ""
        index1 = 0

        if len(line) > 0 and line[0] == ';':
            return
        else:
            index1 = line.index(" ", 0)  # index of first space - Entry1
            Entry1 = line[:index1].strip()
            Entry2 = line[index1 + 1:].strip()

        if table == 0:
            dict.append(TableAB(Entry1, Entry2))
        elif table == 1:
            dict.append(TableBC(Entry1, Entry2))
        else:
            dict.append(TableAC(Entry1, Entry2))

    def dicParser(self, line, dict):
        lemmaID = ""
        entry = ""
        voc = ""
        cat = ""
        gloss = ""
        POS = ""
        index1 = 0
        index2 = 0

        if len(line) > 1 and line[0] == ';':
            lemmaID = line[2:]  # Extracting lemma.
            return
        else:
            index1 = line.index("\t")  # index of first tab - Entry
            entry = line[:index1].strip()
            index2 = line.index("\t", index1 + 1)  # index of second tab - Voc
            voc = line[index1 + 1:index2].strip()
            index1 = line.index("\t", index2 + 1)  # index of third tab - Cat
            cat = line[index2 + 1:index1].strip()
            gloss = line[index1 + 1:].strip()

            try:
                index1 = gloss.index("<pos>", 0)
                if index1 >= 0:
                    a = gloss.index('/', index1 + 1)
                    b = gloss.rindex("</pos>")
                    POS = gloss[a + 1:b].strip()
                    gloss = gloss[:index1].strip()
            except ValueError:
                if cat.startswith("Pref-0") or cat.startswith("Suff-0"):
                    POS = ""
                elif cat.startswith("F"):
                    POS = "FUNC_WORD"
                elif cat.startswith("IV"):
                    POS = "VERB_IMPERFECT"
                elif cat.startswith("PV"):
                    POS = "VERB_PERFECT"
                elif cat.startswith("CV"):
                    POS = "VERB_IMPERATIVE"
                elif cat.startswith("N") and gloss[0].isalpha() and gloss[0].isupper():
                    POS = "NOUN_PROP"
                elif cat.startswith("N") and voc.endswith("ly~"):
                    POS = "NOUN"
                elif cat.startswith("N"):
                    POS = "NOUN"

        dict.append(Dictionary(entry, voc, cat, gloss, POS))


class TableAB:
    def __init__(self, entry1, entry2):
        self.Entry1 = entry1
        self.Entry2 = entry2


class TableBC:
    def __init__(self, entry1, entry2):
        self.Entry1 = entry1
        self.Entry2 = entry2


class TableAC:
    def __init__(self, entry1, entry2):
        self.Entry1 = entry1
        self.Entry2 = entry2


class Dictionary:
    def __init__(self, entry, voc, cat, gloss, POS):
        self.Entry = entry
        self.Voc = voc
        self.Cat = cat
        self.Gloss = gloss
        self.POS = POS
