


class Check(object):
    @staticmethod
    def execute_prim(path, name, contexts):
        args = {}
        for hg, context in enumerate(contexts):
            inst = context.pop(0)
            # print(inst)
            if inst == "RUN":
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
                    tag = "{}:{}".format(str(hg), str(wd))
                    args[tag] = command
            else:
                context.insert(0, inst)
                commands = [context]
                for wd, command in enumerate(commands):
                    tag = "{}:{}".format(str(hg), str(wd))
                    args[tag] = command
        return args

    @staticmethod
    def save_json(file_path, file_name, data):
        path = "{}/{}.json".format(file_path, file_name)

