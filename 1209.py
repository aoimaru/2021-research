import glob
import os
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
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    data = []
    for file_path in file_paths[:100]:
        primitive = Primitive(file_path)
        data = primitive.data
        layers = Structure.toLayer(data, file_path)
        tagged_data = tagging(file_path, layers)
        for key, value in tagged_data.items():
            print(key ,value)
            


def doc2vecs_test():
    hash_code = "8e7af6d92f0a007015d1fe88aab8f8b1570341a1bd2e50d1e315e34d44ac6bdd"

    model = Doc2Vec.load("libs/D2Vs/default-2021-12-06 15:14:57.995406.model")
    sim_items = model.most_similar("673a772d06993b90aade78bc4c5816e69056b75d5cbce3ed2ffb87720b011cd7")
    for sim_item in sim_items:
        print(sim_item)

def main():
    doc2vecs()

if __name__ == "__main__":
    main()
