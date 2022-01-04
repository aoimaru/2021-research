
import dockerfile
import re
import hashlib
import copy

URL_RE_PATTERN = "https?://[^/]+/"

class Dockerfile(object):
    def __init__(self, file_path):
        CHECKS = [
            "TAB",
            "QUATE",
            "NEWLINE"
        ]

        def tab(token):
            # print("token:", token)
            token = list(token)
            words = []
            word = ""
            while token:
                one = token.pop(0)
                word += one
                if word == "\\t":
                    words.append("TAB")
                    word = ""
                else:
                    if not word == "\\":
                        words.append(word)
            args = []
            while words:
                arg = words.pop(0)
                if not arg == "TAB":
                    words.insert(0, arg)
                    break
                args.append(arg)
            # print("words", words)
            if words:
                args.append(words[-1])
            return args
        
        def line(scripts):
            args = []
            for script in scripts:
                words = []
                # print("script", script)
                if script.startswith("'"):
                    comp = copy.copy(script[1:])
                    words.append(comp)
                if bool(re.search(URL_RE_PATTERN, script)):
                    # continue
                    # words.append(script)

                    flag5 = 0
                    if "=" in script:
                        comps = script.split("=")
                        words.append(comps[0])
                        words.append("EQUAL")
                        script = comps[1]
                        if script.endswith(";"):
                            script = script[:-1]
                            flag5 = 1
                        if script.startswith("\\"):
                            script = script[1:]
                        if script.endswith("\\"):
                            script = script[:-1]

                    flag1 = 0
                    flag2 = 0
                    flag3 = 0
                    flag4 = 0
                    if script.startswith("'"):
                        flag1 = 1
                        script = script[1:]
                    if script.startswith('"'):
                        flag2 = 1
                        script = script[1:]
                    if script.endswith("'"):
                        flag3 = 1
                        script = script[:-1]
                    if script.endswith('"'):
                        flag4 = 1
                        script = script[:-1]
                    if flag1 == 1:
                        words.append("QUATE")
                    if flag2 == 1:
                        words.append("QUATE")
                    words.append(script)
                    if flag3 == 1:
                        words.append("QUATE")
                    if flag4 == 1:
                        words.append("QUATE")
                    if flag5 == 1:
                        words.append("AND")

                word = ""
                # print(script)
                script = list(script)
                sub = copy.copy(script)
                while script:
                    one = script.pop(0)
                    # word += one
                    if one == "'":
                        if word:
                            words.append(word)
                        words.append("QUATE")
                        word = ""
                    elif one == '"':
                        if word:
                            words.append(word)
                        words.append("QUATE")
                        word = ""
                    elif one == "(":
                        if word:
                            words.append(word)
                        words.append("LEFT")
                        word = ""
                    elif one == "[":
                        if word:
                            words.append(word)
                        words.append("LEFT")
                        word = ""
                    elif one == "{":
                        if word:
                            words.append(word)
                        words.append("LEFT")
                        word = ""
                    elif one == ")":
                        if word:
                            words.append(word)
                        words.append("RIGHT")
                        word = ""
                    elif one == "]":
                        if word:
                            words.append(word)
                        words.append("RIGHT")
                        word = ""
                    elif one == "}":
                        if word:
                            words.append(word)
                        words.append("RIGHT")
                        word = ""
                    elif one == "$":
                        if word:
                            words.append(word)
                        words.append("DULL")
                        word = ""
                    elif one == "=":
                        if word:
                            words.append(word)
                        words.append("EQUAL")
                        word = ""
                    elif one == "\\":
                        if word:
                            words.append(word)
                        words.append("NEWLINE")
                        word = ""
                    elif one == "TAB":
                        if word:
                            words.append(word)
                        words.append("TAB")
                        word = ""
                    elif one == ";":
                        if word:
                            words.append(word)
                        words.append("AND")
                        word = ""
                    elif one == "&&":
                        if word:
                            words.append(word)
                        words.append("AND")
                        word = ""
                    
                    # elif one == "*":
                    #     if word:
                    #         words.append(word)
                    #     words.append("ASTA")
                    #     word = ""
                    else:
                        word += one
                if not words:
                    words = ["".join(sub)]
                # print(words)
                ans = []
                for word in words:
                    if word == "&&":
                        ans.append("AND")
                    else:
                        ans.append(word)
                args.extend(ans)     
            return args

        def chain(comps):
            words = []
            word = []
            while comps:
                token = comps.pop(0)
                if token == "AND":
                    words.append(word)
                    word = []
                else:
                    word.append(token)

            return words
            
        def to_shell(scripts):
            tokens = scripts.split()
            # print("tokens", tokens)
            # print()
            comps = []
            while tokens:
                token = tokens.pop(0)
                if token.startswith("\\t"):
                    # token = re.sub("\t", " TAB ", token)
                    token = tab(token)
                else:
                    token = [token]
                args = line(token)
                comps.extend(args)
            # print("comps", comps)
                # print(type(token))
            return comps
                
        try:
            self._contents = dockerfile.parse_file(file_path)
        except Exception as e:
            print(e)
            self._contents = []
        self._comped = []
        self._layers = []
        for content in self._contents:
            layers = [content.cmd]
            tokens = list(content.value)
            while tokens:
                layers.append(repr(tokens.pop(0)))
            self._comped.append(layers)
        for layer in self._comped:
            if layer[0] == "RUN":
                comps = to_shell(layer[1])
                comps.insert(0, "RUN")
                coom = copy.copy(comps)
                self._layers.append(coom)
                words = chain(comps)
                # for word in words:
                #     print(word)
            else:
                comps = to_shell(layer[1])
                comps.insert(0, layer[0])
                self._layers.append(comps)

        self._primitives = []
        for layer in self._layers:
            comp = [comp for comp in layer if not comp in CHECKS]
            self._primitives.append(comp)

    @property
    def contents(self):
        return self._contents
    
    @property
    def layers(self):
        return self._layers
    
    @property
    def primitives(self):
        return self._primitives

class Dockerfile_sec(object):
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


