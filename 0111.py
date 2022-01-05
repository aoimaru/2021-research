import glob
import os
import hashlib
import json
import re

from gensim.models import word2vec

from libs.dockerfiles import Dockerfile
from libs.primitives import Primitive
from libs.structures import Structure
from libs.doc2vecs import D2V
from libs.consts import Const, INSTRUCTIONS
from libs.graphs import Graph
from libs.word2vecs import W2V

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

from libs.checks import Check
from libs.names import Name
 

FILEPATH = "./python/3.7/bullseye/slim/Dockerfile"
FILEPATH2 = "./golang/1.16/alpine3.13/Dockerfile"

PYTHON_PROJECT = "./python/**"
GOLANG_PROJECT = "./golang/**"
OTHERS_PROJECT = "./Others/**"

URL_RE_PATTERN = "https?://[^/]+/"

class Dockerfile2(object):

    def __init__(self, file_path):
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
        
    @property
    def contents(self):
        return self._contents
    
    @property
    def layers(self):
        return self._layers

BINNACLE_PROJECT = "./binnacle-icse2020/**"

def test():
    file_paths = [comp for comp in glob.glob(BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    training_data = {}
    for file_path in file_paths:
        df = Dockerfile(file_path)
        primitives = df.primitives
        data = Check.execute_prim("file", file_path, primitives)
        file_name = Name.file_path_to_name(file_path)
        for key, value in data.items():
            print("{}:{}".format(file_name, key), value)
        Check.save_json("./check/BINNACLE/prim", file_name, data)

def main():
    test()
    






if __name__ == "__main__":
    main()