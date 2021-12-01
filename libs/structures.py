import copy
import hashlib

class Structure(object):
    @staticmethod
    def toStack(lines):
        response = []
        # res = []
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
                    comps = comps.split("AND")
                    for comp in comps:
                        if comp:
                            comped.append(comp)
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

        
            
                

                    
                        









                


