import copy
import hashlib

INSTRUCTIONS = [
    "MAINTAINER",
    "RUN",
    "CMD",
    "ENTRYPOINT",
    "LABEL",
    "EXPOSE",
    "ENV",
    "ADD",
    "COPY",
    "VOLUME",
    "USER",
    "WORKDIR",
    "ARG",
    "ONBUILD",
    "STOPSIGNAL",
    "HEALTHCHECK",
    "SHELL"
]

class Structure(object):
    @staticmethod
    def toLayer(comps, file_path):
        layers = []
        layer = []
        while comps:
            comp = comps.pop(0)
            if not comp:
                continue
            if comp[0] in INSTRUCTIONS:
                layers.append(layer)
                layer = []
                layer.append(comp)
            else:
                layer.append(comp)
        return layers
        
    @staticmethod
    def toStack(lines):
        res = []
        def Floor(data):
            indent = 0
            while data:
                word = data.pop(0)
                indent += 1
                if not word == "NL":
                    data.insert(0, word)
                    indent -= 1
                    break
            return indent, data
        comps = []
        for line in lines:
            if not line:
                continue
            indent, line = Floor(line)
            if indent == 0:
                root = line.pop(0)
                comps.append([0, [root]])
                comps.append([1, line])
            else:
                comps.append([indent, line])

        tag = 0
        stacks = []
        if not comps:
            continue
        root = comps.pop(0)
        stacks.append(root[1])
        for comp in comps:
            if comp[0] > tag:
                stacks.append(comp[1])
                tag = comp[0]
            else:
                while True:
                    if len(stacks) <= comp[0]:
                        break
                    stacks.pop(-1)
                stacks.append(comp[1])
                tag = comp[0]
            com = []
            for stack in stacks:
                com.extend(stack)
            copied = copy.copy(com)
            res.append(copied)
        return res


    @staticmethod
    def toStack_old(lines):
        print("lines")
        response = []
        # res = []
        def floor(data):
            indent = 0
            while data:
                word = data.pop(0)
                indent += 1
                if not word == "NL":
                    data.insert(0, word)
                    indent -= 1
                    break
            return indent, data

        # RUNなどのDocker構文を分割
        comps = []
        for line in lines:
            if not line:
                continue
            indent, line = floor(line)
            if indent == 0:
                root = line.pop(0)
                comps.append([0, root])
                line = " ".join(line)
                comps.append([1, line])
            else:
                line = " ".join(line)
                comps.append([indent, line])

        # レイヤーごとに分割
        layers = []
        layer = []
        while comps:
            comp = comps.pop(0)
            if comp[0] == 0:
                layers.append(layer)
                layer = []
            layer.append(comp)
        
        hash_dict = {}
        # スタックでの管理
        for layer in layers:
            # print()
            stack = []
            tag = 0
            if not layer:
                continue
            root = layer.pop(0)
            stack.append(root[1])
            res = []
            for com in layer:
                if com[0] > tag:
                    stack.append(com[1])
                    tag = com[0]
                else:
                    while True:
                        if len(stack) <= com[0]:
                            break
                        stack.pop(-1)
                    stack.append(com[1])
                    tag = com[0]
                # print("stack:", stack)
                copied = copy.copy(stack)

                comped = []
                for comps in copied:
                    comps = comps.split()
                    for comp in comps:
                        # comped.append("AND")
                        if comp:
                            comped.append(comp)
                # comped.pop(0)
                # 
                # comped.pop(1)
                copied = [comp for comp in comped]

                rs = " ".join(copied)
                hash_object = hashlib.sha256(rs.encode()).hexdigest()
                if not hash_object in res:
                    res.append(hash_object)
                hash_dict[hash_object] = copied
            response.append(res)
        return response, hash_dict
    

    @staticmethod
    def toJson(lines):
        res = []
        def floor(data):
            indent = 0
            while True:
                word = data.pop(0)
                indent += 1
                if not word == "NL":
                    data.insert(0, word)
                    indent -= 1
                    break
            return indent, data

        # RUNなどのDocker構文を分割
        comps = []
        for line in lines:
            indent, line = floor(line)
            if indent == 0:
                root = line.pop(0)
                comps.append([0, root])
                line = " ".join(line)
                comps.append([1, line])
            else:
                line = " ".join(line)
                comps.append([indent, line])

        # レイヤーごとに分割
        layers = []
        layer = []
        while comps:
            comp = comps.pop(0)
            if comp[0] == 0:
                layers.append(layer)
                layer = []
            layer.append(comp)

        # スタックでの管理
        for layer in layers:
            print()
            stack = []
            tag = 0
            if not layer:
                continue
            root = layer.pop(0)
            stack.append(root[1])
            res = []
            hash_dict = {}
            for com in layer:
                if com[0] > tag:
                    stack.append(com[1])
                    tag = com[0]
                else:
                    while True:
                        if len(stack) <= com[0]:
                            break
                        stack.pop(-1)
                    stack.append(com[1])
                    tag = com[0]
                # print("stack:", stack)
                copied = copy.copy(stack)
                rs = " ".join(copied)
                hash_object = hashlib.sha256(rs.encode()).hexdigest()
                if not hash_object in res:
                    res.append(hash_object)
                hash_dict[hash_object] = copied

            for rs in res:
                print(hash_dict[rs])
        
    @staticmethod
    def toToken(contents):
        tokens = []
        for content in contents:
            content = content.split()
            while content:
                word = content.pop(0)
                if word:
                    tokens.append(word)
        return tokens
    
    @staticmethod
    def options(tokens):
        res = []
        for token in tokens:
            if len(token) <= 1:
                res.append(token)
            elif token[0] == "-" and token[1] != "-":
                token = list(token)
                root = token.pop(0)
                while token:
                    tk = root + root + token.pop(0)
                    res.append(tk)
            else:
                res.append(token)

        return res
    
    @staticmethod
    def And(tokens):
        if not tokens:
            return tokens
        res = [tokens.pop(0)]
        while tokens:
            token = tokens.pop(0)
            res.append(token)
            res.append("AND")
        res.pop(-1)
        return res
    
    @staticmethod
    def Equal(tokens):
        def rm_crn(word):
            if word.startswith('"'):
                word = word[1:]
            if word.endswith('"'):
                word = word[:-1]
            if word.startswith("'"):
                word = word[1:]
            if word.endswith("'"):
                word = word[:-1]
            return word

        if not tokens:
            return tokens
        res = [tokens.pop(0)]
        while tokens:
            token = tokens.pop(0)
            if not "=" in token:
                res.append(rm_crn(token))
            else:
                token = token.split("=")
                step = []
                for word in token:
                    word = rm_crn(word)
                    step.append(word)
                    step.append("=")
                step.pop(-1)
                res.extend(step)
        return res
    
    @staticmethod
    def toArchitect(responses, hash_dict):
        for order, response in enumerate(responses):
            for column, res in response:
                pass






        
            
                

                    
                        









                


