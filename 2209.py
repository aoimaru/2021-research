import glob
import os
import hashlib
import json

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

PYTHON_PROJECT = "./python/**"
OTHERS_PROJECT = "./Others/**"
GOLANG_PROJECT = "./golang/**"
BINNACLE_PROJECT = "./binnacle-icse2020/**"
DEBIAN_BINNACLE_PROJECT = "./debian-binnacle-icse2020/**"

def tagging(file_path, layers):
    DEL = 1
    file_path = file_path[DEL:]
    res = {}
    for hg, layer in enumerate(layers):
        responses = Structure.toStack(layer)
        for wd, response in enumerate(responses):
            response = Structure.toToken(response)
            response = Structure.Equal(response)
            tag_name = "{}/{}/{}".format(file_path, str(hg), str(wd))
            res[tag_name] = response
    return res


def doc2vecs():
    file_paths = [comp for comp in glob.glob(DEBIAN_BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    training_data = {}
    for file_path in file_paths[:20]:
        print(file_path)
        df = Dockerfile(file_path)
        layers = df.layers
        for layer in layers:
            print(layer)



def main():
    doc2vecs()

    # doc2vecs_test()




if __name__ == "__main__":
    main()
