


class Check(object):
    @staticmethod
    def execute_prim(path, name, contexts):
        for hg, context in enumerate(contexts):
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
                commands = []
                while ops:
                    command = ops.pop(0)
                    if command:
                        command.insert(0, inst)
                        commands.append(command)
                for wd, command in enumerate(commands):
                    print(hg, wd, command)
            else:
                context.insert(0, inst)
                commands = [context]
                for wd, command in enumerate(commands):
                    print(hg, wd, command)


