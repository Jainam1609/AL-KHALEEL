from DicTable import DicTable
# from Segment import Segment


class Segment:
    def __init__(self, prefix, stem, suffix):
        self.Prefix = prefix
        self.Stem = stem
        self.Suffix = suffix

# class DicTable:
#     dictPrefixes = DicTable.dictPrefixes
#     dictStems = DicTable.dictStems
#     dictSuffixes = DicTable.dictSuffixes


DicTable().loadTableAB()
DicTable().loadTableBC()
DicTable().loadTableAC()
DicTable().loadDictionaries()
# print(DicTable.dictPrefixes)
# print(DicTable.dictStems)
# print(DicTable.dictSuffixes)


class Analyzer:
    englishCode = ",;?'|OWI}AbptvjHxd*rzs^SDTZEg_fqklmnhwYyFNKaui~o:PVG0123456789"
    arabicUnicode = "\u060c\u061b\u061f\u0621\u0622\u0623\u0624\u0625\u0626\u0627\u0628\u0629\u062a\u062b\u062c\u062d\u062e\u062f" \
                    "\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063a\u0640\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u0649\u064a\u064b" \
                    "\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670\u067e\u06a4\u06af\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f6\u06f9"

    @staticmethod
    def transliterate(arabicString):
        strEnglish = ""
        for char in arabicString:
            index = Analyzer.arabicUnicode.find(char)
            if index != -1:
                strEnglish += Analyzer.englishCode[index]
            else:
                strEnglish += char
        return strEnglish

    @staticmethod
    def deTransliterate(englishString):
        strArabic = ""
        for char in englishString:
            index = Analyzer.englishCode.find(char)
            if index != -1:
                strArabic += Analyzer.arabicUnicode[index]
            else:
                strArabic += char
        return strArabic

    @staticmethod
    def findIndex(ch, codes):
        for i in range(len(codes)):
            if codes[i] == ch:
                return i
        return -1

    @staticmethod
    def segment(string):
        segments = []

        prefixLength = 0
        suffixLength = 0
        stemLength = 0
        stringLength = len(string)
        prefix = ""
        stem = ""
        suffix = ""
        prefixLengthCheck = 4

        string = Analyzer.transliterate(string)

        if stringLength <= 4:
            prefixLengthCheck = stringLength - 1

        while prefixLength <= prefixLengthCheck:
            prefix = string[0:prefixLength]
            stemLength = stringLength - prefixLength
            suffixLength = 0

            while stemLength >= 1 and suffixLength <= 6:
                stem = string[prefixLength:prefixLength + stemLength]
                suffix = string[prefixLength +
                                stemLength:prefixLength + stemLength + suffixLength]
                segments.append(Segment(prefix, stem, suffix))

                stemLength -= 1
                suffixLength += 1

            prefixLength += 1

        return segments

    @staticmethod
    def validateSegments(segments):
        validSegments = []

        prefixSize = len(DicTable.dictPrefixes)
        stemSize = len(DicTable.dictStems)
        suffixSize = len(DicTable.dictSuffixes)

        if prefixSize == 0 or stemSize == 0 or suffixSize == 0:
            print("Error: Dictionaries are empty.",
                  prefixSize, suffixSize, stemSize)
            return validSegments

        for segment in segments:
            prefixFound = True
            stemFound = True
            suffixFound = True

            # Check the type of segment.Prefix, segment.Stem, and segment.Suffix
            prefix_type = type(segment.Prefix)
            # print(prefix_type)
            stem_type = type(segment.Stem)
            suffix_type = type(segment.Suffix)

            DicTable.dictPrefixes[0] = str(DicTable.dictPrefixes[0])
            dict_prefix_type = type(DicTable.dictPrefixes[0])
            # print(dict_prefix_type)
            DicTable.dictStems[0] = str(DicTable.dictStems[0])
            dict_stem_type = type(DicTable.dictStems[0])
            DicTable.dictSuffixes[0] = str(DicTable.dictPrefixes[0])
            dict_suffix_type = type(DicTable.dictSuffixes[0])

            if prefix_type != dict_prefix_type or stem_type != dict_stem_type or suffix_type != dict_suffix_type:
                print("Type mismatch: Segment properties do not match dictionary types.")
                continue
            if len(segment.Prefix) > 0:
                for i in range(prefixSize):
                    if segment.Prefix == DicTable.dictPrefixes[i]:
                        prefixFound = True
                        break
            else:
                prefixFound = True
            if len(segment.Stem) > 0:
                for i in range(stemSize):
                    if segment.Stem == DicTable.dictStems[i]:
                        stemFound = True
                        break
            else:
                stemFound = True

            if len(segment.Suffix) > 0:
                for i in range(suffixSize):
                    if segment.Suffix == DicTable.dictSuffixes[i]:
                        suffixFound = True
                        break
            else:
                suffixFound = True

            if prefixFound and stemFound and suffixFound:
                validSegments.append(segment)

        return validSegments

    @staticmethod
    def findSolutions(validSegments):
        solutions = []
        prefixSize = len(DicTable.dictPrefixes)
        stemSize = len(DicTable.dictStems)
        suffixSize = len(DicTable.dictSuffixes)

        for segment in validSegments:
            prefixCat = None
            stemCat = None
            suffixCat = None
            refDSPrefix = None
            refDSSuffix = None
            refDSStem = None

            if len(segment.Prefix) == 0:
                prefixCat = "Pref-0"
            else:
                for i in range(prefixSize):
                    try:
                        if segment.Prefix == DicTable.dictPrefixes[i].Entry:
                            prefixCat = DicTable.dictPrefixes[i].Cat
                            refDSPrefix = DicTable.dictPrefixes[i]
                            break
                    except:
                        print(i, "1")
                        continue

            if len(segment.Suffix) == 0:
                suffixCat = "Suff-0"
            else:
                for i in range(suffixSize):
                    try:
                        if segment.Suffix == DicTable.dictSuffixes[i].Entry:
                            suffixCat = DicTable.dictSuffixes[i].Cat
                            refDSSuffix = DicTable.dictSuffixes[i]
                            break
                    except:
                        print(i, "2")
                        continue

            if prefixCat == "Pref-0" and suffixCat == "Suff-0":
                for i in range(stemSize):
                    try:
                        if segment.Stem == DicTable.dictStems[i].Entry:
                            stemCat = DicTable.dictStems[i].Cat
                            refDSStem = DicTable.dictStems[i]
                            solutions.append((segment.Prefix, segment.Stem, segment.Suffix, DicTable.dictStems[i].Entry,
                                              DicTable.dictStems[i].Voc, DicTable.dictStems[i].Gloss, DicTable.dictStems[i].POS))
                            break
                    except AttributeError:
                        print(
                            f"AttributeError: Entry attribute (stem word) not found in DicTable.dictStems[{i}]")
            else:
                for i in range(stemSize):
                    try:
                        if segment.Stem == DicTable.dictStems[i].Entry:
                            print(1)
                            stemCat = DicTable.dictStems[i].Cat
                            print(2)
                            refDSStem = DicTable.dictStems[i]
                            print(3)
                            a = Analyzer.isPairFoundAB(
                                segment.Prefix, DicTable.dictStems[i].Cat)
                            print(a)
                            b = Analyzer.isPairFoundBC(
                                DicTable.dictStems[i].Cat, segment.Suffix)
                            print(b)
                            print(len(DicTable.tableAB))
                            print(len(DicTable.tableBC))
                            print(len(DicTable.tableAC))
                            if a and b:
                                print(segment.Prefix)
                                print(segment.Stem)
                                print(segment.Suffix)
                                print(DicTable.dictStems[i].Entry)
                                print(DicTable.dictStems[i].Voc)
                                print(DicTable.dictStems[i].Gloss)
                                print(DicTable.dictStems[i].POS)
                                solutions.append((segment.Prefix, segment.Stem, segment.Suffix, DicTable.dictStems[i].Entry,
                                                  DicTable.dictStems[i].Voc, DicTable.dictStems[i].Gloss, DicTable.dictStems[i].POS))
                            break
                    except AttributeError:
                        print(
                            f"AttributeError: Entry attribute (has suffix or prefix) not found in DicTable.dictStems[{i}]")

            if stemCat:
                print("Stem Category:", stemCat)
            if refDSPrefix:
                print("Reference DS Prefix:", refDSPrefix.Entry)
            if refDSSuffix:
                print("Reference DS Suffix:", refDSSuffix.Entry)
            if refDSStem:
                print("Reference DS Stem:", refDSStem.Entry)

        return solutions

    @staticmethod
    def isPairFoundAB(prefix, stem):
        for refAB in DicTable.tableAB:
            if stem == refAB.Entry2 and prefix in refAB.Entry1:
                # print("stem found")
                # print(prefix, refAB.Entry1, prefix in refAB.Entry1)
                return True
        return False

    @staticmethod
    def isPairFoundBC(stem, suffix):
        for refBC in DicTable.tableBC:
            if stem == refBC.Entry1 and suffix in refBC.Entry2:
                return True
        return False

    @staticmethod
    def isPairFoundAC(prefix, suffix):
        for refAC in DicTable.tableAC:
            if prefix in refAC.Entry1 and suffix in refAC.Entry2:
                return True
        return False
