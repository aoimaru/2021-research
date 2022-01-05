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

import random
 

FILEPATH = "./python/3.7/bullseye/slim/Dockerfile"
FILEPATH2 = "./golang/1.16/alpine3.13/Dockerfile"

PYTHON_PROJECT = "./python/**"
GOLANG_PROJECT = "./golang/**"
OTHERS_PROJECT = "./Others/**"

URL_RE_PATTERN = "https?://[^/]+/"

BINNACLE_PROJECT = "./binnacle-icse2020/**"
DEBIAN_BINNACLE_PROJECT = "./debian/**"

def binnacle_to_json():
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

def subPython():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths:
        rnd = "".join(map(str, [random.randint(0, 9) for _ in range(9)]))
        file_name = Name.file_path_to_name(file_path)
        df = Dockerfile(file_path)
        layers = df.layers
        data = Check.execute_prim("file", file_path, layers)
        Check.save_json("./check/python/tab", "{}.Dockerfile".format(rnd), data)
    
def debian_binnacle_to_json():
    file_paths = [comp for comp in glob.glob(DEBIAN_BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    training_data = {}
    for file_path in file_paths:
        df = Dockerfile(file_path)
        primitives = df.primitives
        data = Check.execute_prim("file", file_path, primitives)
        file_name = Name.file_path_to_name(file_path)
        for key, value in data.items():
            print("{}:{}".format(file_name, key), value)
        Check.save_json("./check/Debian/prim", file_name, data)

def main():
    # test()
    # subPython()
    






if __name__ == "__main__":
    main()