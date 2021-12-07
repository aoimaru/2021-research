
import dockerfile
import re
import hashlib

URL_RE_PATTERN = "https?://[^/]+/"

class Dockerfile(object):
    def __init__(self, file_path):

        def norm(token):
            """
                "とか'を削除
            """
            if token.startswith('"'):
                token = token[1:]
            if token.endswith('"'):
                token = token[:-1]
            if token.startswith("'"):
                token = token[1:]
            if token.endswith("'"):
                token = token[:-1]
            return token

        def to_methods(scripts):
            scripts = re.sub("\n", " NL ", scripts)
            scripts = re.sub("\t", " NL ", scripts)
            scripts = re.sub(";", " AND ", scripts)
            scripts = re.sub("&&", " AND ", scripts)

            tokens = ["RUN"] + [token.lstrip().rstrip() for token in scripts.split()]
            

            Res = []
            while tokens:
                word = tokens.pop(0)
                if bool(re.search(URL_RE_PATTERN, word)):
                    word = norm(word)
                    Res.append(word)
                else:
                    if word == "\\(":
                        word = "BACKLEFT"
                        Res.append(word)
                    elif word == "\\)":
                        word = "BACKRIGHT"
                        Res.append(word)
                    elif word == "\\n":
                        word = "BACKNT"
                        Res.append(word)
                    elif word == "(":
                        word = "LEFT"
                        Res.append(word)
                    elif word == "[":
                        word = "LEFT"
                        Res.append(word)
                    elif word == "{":
                        word = "LEFT"
                        Res.append(word)
                    elif word == ")":
                        word = "RIGHT"
                        Res.append(word)
                    elif word == "]":
                        word = "RIGHT"
                        Res.append(word)
                    elif word == "}":
                        word = "RIGHT"
                        Res.append(word)
                    else:
                        if "$(" or "$[" or "${" in word:
                            word = word.replace("$(", " SUBLEFT ")
                            word = word.replace("$[", " SUBLEFT ")
                            word = word.replace("${", " SUBLEFT ")
                        if ")'" or ')"' in word:
                            word = word.replace(")'" , " SUBRIGHT ")
                            word = word.replace(')"', " SUBRIGHT ")

                        words = word.split()
                        for word in words:
                            word = norm(word)
                            backs = []
                            if word == "{}":
                                Res.append(word)
                            elif word.endswith(")") or word.endswith("]") or word.endswith("}"):
                                Res.append(word[:-1])
                                Res.append("SUBRIGHT")
                            else:
                                Res.append(word)

            Res = [norm(res) for res in Res]
            return Res
        try:
            self._contents = dockerfile.parse_file(file_path)
        except:
            self._contents = []

        self._layers = []

        for content in self._contents:
            if content.cmd == "RUN":
                
                Res = to_methods(content.value[0])
                self._layers.append(Res)
            elif content.cmd == "ENV" or "COPY" or "ADD" or "ARG" or "VOLUME":
                self._layers.append([content.cmd]+list(content.value[:2]))
            elif content.cmd == "CMD" or "ENTRYPOINT":
                self._layers.append([content.cmd]+list(content.value))
            else:
                self._layers.append([content.cmd]+list(content.value[0]))

        
    @property
    def contents(self):
        return self._contents


    @property
    def layers(self):
        return self._layers

    
import dockerfile
import re
import hashlib

URL_RE_PATTERN = "https?://[^/]+/"

class Dockerfile_BACKUP(object):
    def __init__(self, file_path):

        def norm(token):
            """
                "とか'を削除
            """
            if token.startswith('"'):
                token = token[1:]
            if token.endswith('"'):
                token = token[:-1]
            if token.startswith("'"):
                token = token[1:]
            if token.endswith("'"):
                token = token[:-1]
            return token


        def to_methods(scripts):
            scripts = re.sub("\n", " NL ", scripts)
            scripts = re.sub("\t", " NL ", scripts)
            scripts = re.sub(";", " AND ", scripts)
            scripts = re.sub("&&", " AND ", scripts)

            tokens = ["RUN"] + [token.lstrip().rstrip() for token in scripts.split()]
            

            Res = []
            while tokens:
                word = tokens.pop(0)
                if bool(re.search(URL_RE_PATTERN, word)):
                    word = norm(word)
                    Res.append(word)
                else:
                    if word == "\\(":
                        word = "BACKLEFT"
                        Res.append(word)
                    elif word == "\\)":
                        word = "BACKRIGHT"
                        Res.append(word)
                    elif word == "\\n":
                        word = "BACKNT"
                        Res.append(word)
                    elif word == "(":
                        word = "LEFT"
                        Res.append(word)
                    elif word == "[":
                        word = "LEFT"
                        Res.append(word)
                    elif word == "{":
                        word = "LEFT"
                        Res.append(word)
                    elif word == ")":
                        word = "RIGHT"
                        Res.append(word)
                    elif word == "]":
                        word = "RIGHT"
                        Res.append(word)
                    elif word == "}":
                        word = "RIGHT"
                        Res.append(word)
                    else:
                        if "$(" or "$[" or "${" in word:
                            word = word.replace("$(", " SUBLEFT ")
                            word = word.replace("$[", " SUBLEFT ")
                            word = word.replace("${", " SUBLEFT ")
                        if ")'" or ')"' in word:
                            word = word.replace(")'" , " SUBRIGHT ")
                            word = word.replace(')"', " SUBRIGHT ")

                        words = word.split()
                        for word in words:
                            word = norm(word)
                            backs = []
                            if word == "{}":
                                Res.append(word)
                            elif word.endswith(")") or word.endswith("]") or word.endswith("}"):
                                Res.append(word[:-1])
                                Res.append("SUBRIGHT")
                            else:
                                Res.append(word)

            Res = [norm(res) for res in Res]
            return Res
        try:
            self._contents = dockerfile.parse_file(file_path)
        except:
            self._contents = []

        self._layers = []

        for content in self._contents:
            if content.cmd == "RUN":

                print("OK")
                Res = to_methods(content.value[0])
                print("Res", Res)
                self._layers.append(Res)
            elif content.cmd == "ENV" or "COPY" or "ADD" or "ARG" or "VOLUME":
                self._layers.append([content.cmd]+list(content.value[:2]))
            elif content.cmd == "CMD" or "ENTRYPOINT":
                self._layers.append([content.cmd]+list(content.value))
            else:
                self._layers.append([content.cmd]+list(content.value[0]))

        self._primitives_key = []
        self._primitives_dict = {}
        for layer in self._layers:
            if not layer[0] == "RUN":
                rs = " ".join(layer)
                hash_object = hashlib.sha256(rs.encode()).hexdigest()
                self._primitives_key.append(hash_object)
                if not hash_object in self._primitives_dict:
                    self._primitives_dict[hash_object] = []
                self._primitives_dict[hash_object].append(layer)
                # self._primitives.append(layer)
            else:
                rs = " ".join(layer)
                layer.pop(0)
                comps = []
                primitive = []
                while layer:
                    comp = layer.pop(0)
                    if comp == "AND":
                        primitive.append(["RUN"]+list(comps))
                        comps = []
                    else:
                        comps.append(comp)
                hash_object = hashlib.sha256(rs.encode()).hexdigest()
                if not hash_object in self._primitives_dict:
                    self._primitives_dict[hash_object] = []
                for comp in primitive:
                    self._primitives_dict[hash_object].append(comp)
                self._primitives_key.append(hash_object)
                # self._primitives.append(primitive)


    @property
    def contents(self):
        return self._contents


    @property
    def layers(self):
        return self._layers

    @property
    def primitives_key(self):
        return self._primitives_key
    
    @property
    def primitives_dict(self):
        return self._primitives_dict


