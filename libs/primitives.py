import re

from libs.exceptions import ReadFileError

class Primitive(object):
    def __init__(self, file_path):
        def back_fix(word):
            return word.replace("\\", "BACK")
        def cmt_fix(word):
            if word.startswith("'"):
                word = word[1:]
            if word.endswith("'"):
                word = word[:-1]
            if word.startswith('"'):
                word = word[1:]
            if word.endswith('"'):
                word = word[:-1]
            return word

        def lr_fix(word):
            if word == "(":
                word = "LEFT"
            if word == "{":
                word = "LEFT"
            if word == "[":
                word = "LEFT"
            if word == ")":
                word = "RIGHT"
            if word == "}":
                word = "RIGHT"
            if word == "]":
                word = "RIGHT"
            
            return word

        try:
            with open(file_path, mode="r") as f:
                lines = f.readlines()
        except Exception as e:
            print(e)
            raise ReadFileError("failed to read file") from e
        else:
            self._data = []
            for line in lines:
                # print("line: ", line)
                line = re.sub("\n", " NL ", line)
                line = re.sub("\t", " NL ", line)
                line = re.sub("&&", " AND ", line)
                line = re.sub(";", " AND ", line)

                line = re.sub("\(", " BACKLEFT ", line)
                line = re.sub("\)", " BACKRIGHT ", line)

                if not line:
                    continue
                if line.startswith("#"):
                    continue
                if line == " NL ":
                    continue
                
                if "$(" or "$[" or "${" in line:
                    line = line.replace("$(", " SUBLEFT ")
                    line = line.replace("$[", " SUBLEFT ")
                    line = line.replace("${", " SUBLEFT ")
                if ")'" or ')"' in line:
                    line = line.replace(")'" , " SUBRIGHT ")
                    line = line.replace(')"', " SUBRIGHT ")

                line = [back_fix(word) for word in line.split()]
                line = [cmt_fix(word) for word in line]
                line = [lr_fix(word) for word in line]

                self._data.append(line)
                
    @property
    def data(self):
        return self._data


class UnionFind(object):
    pass
