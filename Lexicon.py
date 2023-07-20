
import re


class Lexicon:
    def __init__(self):
        self.htLX = {}
        with open("Doc\\nw.txt", encoding='utf-8') as file:
            for line in file:
                keyword, meaning = line.strip().split(":\t")
                self.htLX[self.get_key(keyword)] = meaning

    def get_key(self, keyword):
        i = 1
        temp = keyword
        while temp in self.htLX:
            temp = f"{keyword} {i}"
            i += 1
        return temp

    def search_by_key(self, inword, pattern):
        keywords = []
        if pattern is None:
            temp = inword
            i = 0
            while i <= 9:
                if temp in self.htLX:
                    keywords.append(temp)
                temp = f"{inword} {i}"
                i += 1
                if temp in self.htLX:
                    keywords.append(temp)
            if not keywords:
                i = 0
                temp = f"ال{inword}"
                while i <= 9:
                    if temp in self.htLX:
                        keywords.append(temp)
                    temp = f"ال{inword} {i}"
                    i += 1
        else:  # with regular expression
            regex = re.compile(pattern)
            for key in self.htLX:
                if key[-1].isdigit():
                    if regex.match(key[:-2]):
                        keywords.append(key)
                elif regex.match(key):
                    keywords.append(key)
                else:
                    regex = re.compile(pattern[:1] + "ال" + pattern[1:])
                    if regex.match(key):
                        keywords.append(key)
        return keywords

    def search_by_value(self, inword: str, pattern: str) -> list[str]:
        keywords = []
        if pattern is None:
            for key, value in self.htLX.items():
                subkeywords = self.parse_meaning(value)
                for subkeyword in subkeywords:
                    words = subkeyword.split()
                    if inword in words or f"ال{inword}" in words:
                        keywords.append(key)
                        break
        else:  # with regular expression
            regex = re.compile(pattern)
            for key, value in self.htLX.items():
                subkeywords = self.parse_meaning(value)
                for subkeyword in subkeywords:
                    words = subkeyword.split()
                    for word in words:
                        if regex.match(word):
                            keywords.append(key)
                            break
                        else:
                            regex = re.compile(
                                pattern[:1] + "ال" + pattern[1:])
                            if regex.match(word):
                                keywords.append(key)
                                break
        return keywords

    def search(self, inword, pattern):
        keywords = []
        if self.search_by_key(inword, pattern):
            keywords.extend(self.search_by_key(inword, pattern))
        else:
            keywords.extend(self.search_by_value(inword, pattern))
        return keywords

    def parse_meaning(self, meaning):
        subkeywords = []
        regex = re.compile(r"\( \w+[ \t\w]+ \)")
        matches = regex.findall(meaning)
        for match in matches:
            if " في " not in match and " مج " not in match and " مو " not in match and \
                    " مع " not in match and " محدثة " not in match and " انظر " not in match:
                subkeywords.append(match[2:-2])
        return subkeywords

    def view_meaning(self, meaning):
        str = meaning
        subkeywords = self.parse_meaning(meaning)
        for subkeyword in subkeywords:
            index = str.find("( " + subkeyword + " )")
            if index > 0 and str[index - 1] != '\t':
                str = str[:index] + "\n" + str[index:]
        return str
