import glob
import os

from libs.dockerfiles import Model
from libs.primitives import Primitive
from libs.structures import Structure
from libs.dock2vecs import D2V
from libs.consts import Const, INSTRUCTIONS
from libs.graphs import Graph
from libs.word2vecs import W2V

PYTHON_PROJECT = "./python/**"
OTHERS_PROJECT = "./Others/**"
GOLANG_PROJECT = "./golang/**"
BINNACLE_PROJECT = "./binnacle-icse2020/**"

CNT = Const.book

def test():
    # df = Dockerfile(TEST_PATH)
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths:
        print()
        primitive = Primitive(file_path)
        # print(primitive.data)
        responses, hash_dict = Structure.toStack(primitive.data)
        for response in responses:
            print()
            for res in response:
                # print()
                tokens = hash_dict[res]
                # tokens = Structure.And(tokens)
                tokens = Structure.toToken(tokens)
                
                tokens = Structure.Equal(tokens)
                print(tokens)
    

def test_4():
    # df = Dockerfile(TEST_PATH)
    file_paths = [comp for comp in glob.glob(BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths[:1000]:
        # 
        print()
        primitive = Primitive(file_path)
        # print(primitive.data)
        responses, hash_dict = Structure.toStack(primitive.data)
        for response in responses:

            # 
            # print()
            contents = []
            for res in response:
                tokens = hash_dict[res]
                tokens = Structure.toToken(tokens)
                tokens = Structure.Equal(tokens)
                # print("tokens:", tokens)
                contents.append(tokens)
        
            context = Graph.toContent(contents)
            for con in context:
                print("con:", con)
                trainings.append(con)

    W2V.execute(trainings)
















def test_2():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths[:1]:
        print()
        model = Model(file_path)
        primitives_key = model.primitives_key
        primitives_dict = model._primitives_dict

        for p_key in primitives_key:
            p_items = primitives_dict[p_key]
            print()
            for p_item in p_items:
                tokens = Structure.toToken(p_item)
                tokens = Structure.Equal(tokens)
                print(tokens)

def test_3():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    data = []
    for file_path in file_paths:
        primitive = Primitive(file_path)
        responses, hash_dict = Structure.toStack(primitive.data)
        for response in responses:
            for res in response:
                tokens = hash_dict[res]
                tokens = Structure.toToken(tokens)
                tokens = Structure.Equal(tokens)
                # print(tokens)
                data.append(tokens)
    
    model, hash_dict, hash_key = D2V.execute(data)
    for key, value in hash_dict.items():
        print(key)
    
    
    print(model.docvecs['7ece24f3b6bffa3df20ce8ada18c4ad430db9932045c9ed199cd84be177f0acf'])

    sim_items = model.docvecs.most_similar('7ece24f3b6bffa3df20ce8ada18c4ad430db9932045c9ed199cd84be177f0acf')

    for sim_item in sim_items:
        print(sim_item)
        print(hash_dict[sim_item[0]][0], sim_item[1])


def test_5():
    pass


def main():
    # test_3()
    # test()
    # test_2()
    # test_4()
    test_4()

if __name__ == "__main__":
    main()