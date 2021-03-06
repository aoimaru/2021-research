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
from libs.names import Name, Rnd
from libs.paths import Path
from libs.trs import TR

import random
 

FILEPATH = "./python/3.7/bullseye/slim/Dockerfile"
FILEPATH2 = "./golang/1.16/alpine3.13/Dockerfile"

PYTHON_PROJECT = "./python/**"
GOLANG_PROJECT = "./golang/**"
OTHERS_PROJECT = "./Others/**"

URL_RE_PATTERN = "https?://[^/]+/"

BINNACLE_PROJECT = "./binnacle-icse2020/**"
DEBIAN_BINNACLE_PROJECT = "./debian/**"
UBUNTU_PROJECT = "./ubuntu/**"

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

def ubuntu_to_json():
    file_paths = [comp for comp in glob.glob(UBUNTU_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    training_data = {}
    for file_path in file_paths:
        df = Dockerfile(file_path)
        primitives = df.primitives
        data = Check.execute_prim("file", file_path, primitives)
        file_name = Name.file_path_to_name(file_path)
        for key, value in data.items():
            print("{}:{}".format(file_name, key), value)
        Check.save_json("./check/ubuntu/prim", file_name, data)

def open_json(file_path):
    with open(file_path, mode="r") as f:
        comps = json.load(f)
    return comps



def debian_doc2vecs():
    training_data = {}
    DPATH = "./check/Debian/prim/**"
    file_paths = [comp for comp in glob.glob(DPATH, recursive=True) if os.path.isfile(comp) if comp.endswith(".json")]
    for file_path in file_paths:
        print(file_path)
        file_name = Name.file_path_to_name(file_path)
        rnd = re.sub(".json", "", file_name)
        comps = open_json(file_path)
        for key, value in comps.items():
            res = {}
            tag_name = "{}:{}".format(rnd, key)
            res[tag_name] = value
            training_data.update(res)
    D2V.do(training_data, name="Debian_DM_0_0")

def debian_doc2vecs_test():
    MODEL_PATH = "./libs/D2Vs/Debian_DM_0_0-2022-01-06 01:50:56.962337.model"
    model = Doc2Vec.load(MODEL_PATH)
    key_name = "294394255:8:6"
    name, fst, sec = key_name.split(":")
    sim_items = model.docvecs.most_similar(key_name)
    file_path = "{}/{}.json".format("./check/Debian/prim", name)
    comps = open_json(file_path)
    tag_name = "{}:{}".format(fst, sec)
    print(comps[tag_name])
    print()
    for sim_item in sim_items:
        print()
        print(sim_item)
        name, fst, sec = sim_item[0].split(":")
        file_path = "{}/{}.json".format("./check/Debian/prim", name)
        comps = open_json(file_path)
        tag_name = "{}:{}".format(fst, sec)
        print(comps[tag_name])

def debian_doc2vecs_run():
    training_data = {}
    DPATH = "./check/Debian/prim/**"
    file_paths = [comp for comp in glob.glob(DPATH, recursive=True) if os.path.isfile(comp) if comp.endswith(".json")]
    for file_path in file_paths:
        print(file_path)
        file_name = Name.file_path_to_name(file_path)
        rnd = re.sub(".json", "", file_name)
        comps = open_json(file_path)
        for key, value in comps.items():
            res = {}
            tag_name = "{}:{}".format(rnd, key)
            if value[0] == "RUN":
                res[tag_name] = value
                training_data.update(res)
    D2V.do(training_data, name="Debian_DM_run_0_0_")

def debian_doc2vecs_run_test():
    MODEL_PATH = "./libs/D2Vs/Debian_DM_run_0_0_-2022-01-06 02:16:11.772078.model"
    model = Doc2Vec.load(MODEL_PATH)
    key_name = "345360222:4:2"
    name, fst, sec = key_name.split(":")
    sim_items = model.docvecs.most_similar(key_name)
    file_path = "{}/{}.json".format("./check/Debian/prim", name)
    comps = open_json(file_path)
    tag_name = "{}:{}".format(fst, sec)
    print(comps[tag_name])
    print()
    for sim_item in sim_items:
        print()
        print(sim_item)
        name, fst, sec = sim_item[0].split(":")
        file_path = "{}/{}.json".format("./check/Debian/prim", name)
        comps = open_json(file_path)
        tag_name = "{}:{}".format(fst, sec)
        print(comps[tag_name])



def ubuntu_doc2vecs():
    training_data = {}
    DPATH = "./check/Ubuntu/prim/**"
    file_paths = [comp for comp in glob.glob(DPATH, recursive=True) if os.path.isfile(comp) if comp.endswith(".json")]
    for file_path in file_paths:
        print(file_path)
        file_name = Name.file_path_to_name(file_path)
        rnd = re.sub(".json", "", file_name)
        comps = open_json(file_path)
        for key, value in comps.items():
            res = {}
            tag_name = "{}:{}".format(rnd, key)
            res[tag_name] = value
            training_data.update(res)
    D2V.do(training_data, name="Ubuntu_DM_0_0")

def debian_doc2vecs_test():
    MODEL_PATH = "./libs/D2Vs/Debian_DM_0_0-2022-01-06 01:50:56.962337.model"
    model = Doc2Vec.load(MODEL_PATH)
    key_name = "294394255:8:6"
    name, fst, sec = key_name.split(":")
    sim_items = model.docvecs.most_similar(key_name)
    file_path = "{}/{}.json".format("./check/Debian/prim", name)
    comps = open_json(file_path)
    tag_name = "{}:{}".format(fst, sec)
    print(comps[tag_name])
    print()
    for sim_item in sim_items:
        print()
        print(sim_item)
        name, fst, sec = sim_item[0].split(":")
        file_path = "{}/{}.json".format("./check/Debian/prim", name)
        comps = open_json(file_path)
        tag_name = "{}:{}".format(fst, sec)
        print(comps[tag_name])

def ubuntu_run_doc2vec():
    training_data = {}
    DPATH = "./check/Ubuntu/prim/**"
    file_paths = [comp for comp in glob.glob(DPATH, recursive=True) if os.path.isfile(comp) if comp.endswith(".json")]
    for file_path in file_paths:
        print(file_path)
        file_name = Name.file_path_to_name(file_path)
        rnd = Rnd.get(file_name)
        comps = open_json(file_path)
        for key, value in comps.items():
            res = {}
            tag_name = "{}:{}".format(rnd, key)
            res[tag_name] = value
            training_data.update(res)
    D2V.do(training_data, name="Ubuntu_run_DM_0", model_path="default", dm=0, window=5, min_count=1)

def check():
    file_paths = Path.get_file_path("./check/Ubuntu/prim")
    training_data = TR.runs(file_paths)
    for key, value in training_data.items():
        print(key, value)
    D2V.do(training_data, name="DM_0", distribution="ubuntu", types="runs", dm=0, window=5, min_count=1)
        
def check_test():
    MODEL_PATH = "./libs/Models/ubuntu/runs/DM1/DM_1-2022-01-06 19:40:59.389739.model"
    model = Doc2Vec.load(MODEL_PATH)
    key_name = "146910404:3:0"
    key_name = "146910404:3:2"
    name, fst, sec = key_name.split(":")
    sim_items = model.docvecs.most_similar(key_name)
    file_path = "{}/{}.json".format("./check/Ubuntu/prim", name)
    comps = open_json(file_path)
    tag_name = "{}:{}".format(fst, sec)
    print(comps[tag_name])
    print()
    for sim_item in sim_items:
        print()
        print(sim_item)
        name, fst, sec = sim_item[0].split(":")
        file_path = "{}/{}.json".format("./check/Ubuntu/prim", name)
        comps = open_json(file_path)
        tag_name = "{}:{}".format(fst, sec)
        print(comps[tag_name])



def main():
    # test()
    # subPython()
    # debian_binnacle_to_json()
    # ubuntu_to_json()
    # debian_doc2vecs_test()
    # ubuntu_doc2vecs()
    check_test()






if __name__ == "__main__":
    main()