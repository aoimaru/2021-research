import dockerfile
import re

URL_RE_PATTERN = "https?://[^/]+/"


class Model(object):
    def __init__(self, file_path):
        self._contents = dockerfile.parse_file(file_path)
        # トークンの正規化
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
        # メソッドチェーンやトークン, スペース, 改行コードの正規化
        def method_chain(scripts):
            """
                メソッドチェーンの分割やスペース, 改行コードの正規化
            """
            scripts = re.sub("\n", " NL ", scripts)
            scripts = re.sub("\t", " NL ", scripts)
            scripts = re.sub(";", " AND ", scripts)
            scripts = re.sub("&&", " AND ", scripts)
            scripts = re.sub(" ", " SPACE ", scripts)

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


        self._commands = []
        for content in self._contents:
            if content.cmd == "RUN":
                self._commands.append(method_chain(content.value[0]))
            elif content.cmd == "ENV" or "COPY" or "ADD" or "ARG" or "VOLUME":
                self._commands.append([content.cmd]+list(content.value[:2]))
            elif content.cmd == "CMD" or "ENTRYPOINT":
                self._commands.append([content.cmd]+list(content.value))
            else:
                self._commands.append([content.cmd]+list(content.value[0]))
        
        self._runs = []
        for command in self._commands:
            com = command.pop(0)
            if com == "RUN":
                Req = []
                comp = []
                while command:
                    word = command.pop(0)
                    if word == "AND":
                        comp.insert(-1, "AND")
                        Req.append(comp)
                        comp = []
                    else:
                        comp.append(word)
                Req.pop(-1)
                self._runs.append(Req)

        self._shells = []
        for run in self._runs:
            self._shells.append([])
            for shells in run:
                shells = [shell for shell in shells if shell != "SPACE"]
                shells = [shell for shell in shells if shell != "NT"]
                shells = [shell.replace("(", "") for shell in shells]
                shells = [shell.replace("(", "") for shell in shells]
                shells = [shell.replace(")", "") for shell in shells]
                shells = [shell.replace(")", "") for shell in shells]
                shells = [shell.replace("[", "") for shell in shells]
                shells = [shell.replace("[", "") for shell in shells]
                shells = [shell.replace("]", "") for shell in shells]
                shells = [shell.replace("]", "") for shell in shells]

                shells = [shell.replace("\\n", "BACKNT") for shell in shells]

                shells = [norm(shell) for shell in shells]
                shells = [shell for shell in shells if shell]
                if shells:
                    self._shells.append(shells)


    @property
    def contents(self):
        return self._contents
    
    @property
    def commands(self):
        return self._commands
    
    @property
    def runs(self):
        return self._runs
    
    @property
    def shells(self):
        return self._shells



def main():
    file_path = "../../python/3.10/bullseye/slim/Dockerfile"
    # file_path = "../../Others/Dockerfile"
    model = Model(file_path)
    commands = model.commands
    runs = model.runs
    for run in runs:
        print()
        for shells in run:
            shells = [shell for shell in shells if shell != ("SPACE" or "NT")]
            print(shells)
if __name__ == "__main__":
    main()
    