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

def open_json(file_path):
    """
        patch
    """
    with open(file_path, mode="r") as f:
        comps = json.load(f)
    return comps


def check():
    file_paths = Path.get_file_path("./check/Ubuntu/prim")
    training_data = TR.default(file_paths)
    for key, value in training_data.items():
        print(key, value)
    D2V.do(training_data, name="DM_1", distribution="ubuntu", types="default", dm=1, window=5, min_count=1)
        
def check_test():
    MODEL_PATH = "./libs/Models/ubuntu/default/DM1/DM_1-2022-01-06 20:30:48.335485.model"
    model = Doc2Vec.load(MODEL_PATH)
    # key_name = "146910404:3:0"
    key_name = "146910404:3:2"
    # key_name = "345371063:3:4"
    
    # key_name = "320100973:6:0"
    # key_name = "345379003:3:16"
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
    check_test()


if __name__ == "__main__":
    main()