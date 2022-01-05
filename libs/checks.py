


class Check(object):
    @staticmethod
    def execute_prim(path, name, contexts):
        for context in contexts:
            inst = context.pop(0)
            print(inst)

            if inst == "RUN":
                # print(context)
                ops = []
                op = []
                while context:
                    token = context.pop(0)
                    if token == "AND":
                        ops.append(op)
                        op = []
                    else:
                        op.append(token)
                for op in ops:
                    print(op)
            else:
                print(context)

