import json
from libs.names import Name, Rnd
import pathlib

class TR(object):
    @staticmethod
    def default(file_paths):
        def open_json(path):
            try:
                with open(path, mode="r") as f:
                    comps = json.load(f)
            except Exception as e:
                print(e)
                return []
            else:
                return comps

        training_data = {}
        for file_path in file_paths:
            print(file_path)
            file_name = Name.file_path_to_name(file_path)
            rnd = Rnd.get(file_name)
            comps = open_json(file_path)
            for key, value in comps.items():
                res = {
                    "{}:{}".format(rnd, key): value
                }
                training_data.update(res)
        return training_data

    @staticmethod
    def runs(file_paths):
        def open_json(path):
            try:
                with open(path, mode="r") as f:
                    comps = json.load(f)
            except Exception as e:
                print(e)
                return []
            else:
                return comps

        training_data = {}
        
        for file_path in file_paths:
            print(file_path)
            file_name = Name.file_path_to_name(file_path)
            rnd = Rnd.get(file_name)
            comps = open_json(file_path)
            for key, value in comps.items():
                types = value.pop(0)
                if types == "RUN":
                    res = {
                        "{}:{}".format(rnd, key): value
                    }
                    training_data.update(res)
        return training_data
