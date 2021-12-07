import glob
import os
import hashlib

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
    training_data = {}
    for file_path in file_paths:
        primitive = Primitive(file_path)
        data = primitive.data
        layers = Structure.toLayer(data, file_path)
        tagged_data = tagging(file_path, layers)
        training_data.update(tagged_data)
    D2V.do(training_data, name="new")

def doc2vecs_test():
    def toHash(word):
        hash_object = hashlib.sha256(word.encode()).hexdigest()
        return hash_object
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths:
        print(file_path)
    code = toHash("/python/3.6/alpine3.14/Dockerfile/12/15")
    model = Doc2Vec.load("libs/D2Vs/new-2021-12-07 18:44:28.292220.model")
    sim_items = model.docvecs.doctags
    # sim_items = model.docvecs.similarity("dd5320931121b545c395d98dd14add71a446b3584e19768fdabadd9fa90ba85b", "6a64aec3301521f1d1492da8c05d830f5f16950c90de4264c6cf32a1a53dd909")
    sim_items = model.docvecs.most_similar(code)
    for sim_item in sim_items:
        print(sim_item[0], sim_item[1])
        
    

def main():






    doc2vecs_test()



if __name__ == "__main__":
    main()
