
import dockerfile
import re

URL_RE_PATTERN = "https?://[^/]+/"

class News(object):
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

        self._contents = dockerfile.parse_file(file_path)

        self._layers = []
        for content in self._contents:
            if content.cmd == "RUN":
                self._layers.append(to_methods(content.value[0]))
            elif content.cmd == "ENV" or "COPY" or "ADD" or "ARG" or "VOLUME":
                self._layers.append([content.cmd]+list(content.value[:2]))
            elif content.cmd == "CMD" or "ENTRYPOINT":
                self._layers.append([content.cmd]+list(content.value))
            else:
                self._layers.append([content.cmd]+list(content.value[0]))

        self._primitives = []
        for layer in self._layers:
            if not layer[0] == "RUN":
                self._primitives.append(layer)
            else:
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
                self._primitives.append(primitive)


    @property
    def contents(self):
        return self._contents


    @property
    def layers(self):
        return self._layers

    @property
    def primitives(self):
        return self._primitives

