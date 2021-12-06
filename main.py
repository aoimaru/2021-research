import glob
import os
from gensim.models import word2vec

from libs.dockerfiles import Dockerfile
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
DEBIAN_BINNACLE_PROJECT = "./debian-binnacle-icse2020/**"

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

def test_9():
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
        
            context_before = Graph.toContent(contents)
            context_after = Graph.toContentAfter(contents)
            for before, after in zip(context_before, context_after):
                trainings.append(before)
                trainings.append(after)

    W2V.execute(trainings, "before-after")

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
    
    
    print(model.docvecs['83b65817171365b31fe9538d8bd98bca800b35bbbca8f9df22e9f96219dfb0ed'])

    sim_items = model.docvecs.most_similar('83b65817171365b31fe9538d8bd98bca800b35bbbca8f9df22e9f96219dfb0ed')

    for sim_item in sim_items:
        print(sim_item)
        print(hash_dict[sim_item[0]][0], sim_item[1])

def test_5():
    path = "./libs/delv/default-2021-12-04 08:58:24.615672.model"

    model = word2vec.Word2Vec.load(path)

    similar_words = model.wv.most_similar(positive=["apt-get", "install"], topn=9)

    for similar_word in similar_words:

        print(similar_word)

def test_6():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths:
        model = Model(file_path)
        primitives_key = model.primitives_key
        primitives_dict = model._primitives_dict

        for p_key in primitives_key:
            p_items = primitives_dict[p_key]
            for p_item in p_items:
                tokens = Structure.toToken(p_item)
                tokens = Structure.Equal(tokens)
                # print(tokens)
                trainings.append(tokens)
    
    W2V.execute(trainings, "naivePython")

def test_8():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths:
        model = Model(file_path)
        primitives_key = model.primitives_key
        primitives_dict = model._primitives_dict

        for p_key in primitives_key:
            p_items = primitives_dict[p_key]
            for p_item in p_items:
                tokens = Structure.toToken(p_item)
                tokens = Structure.Equal(tokens)
                # print(tokens)
                trainings.append(tokens)
    
    W2V.execute(trainings, "naivePython")

def test_7():
    path = "./libs/delv/naivePython-2021-12-04 10:49:46.705357.model"

    model = word2vec.Word2Vec.load(path)
    similar_words = model.wv.most_similar(positive=["apt-get", "install"], topn=10)
    for similar_word in similar_words:

        print(similar_word)

def test_10():
    """
    前後の関係を考慮したモデルの結果
    """
    path = "./libs/delv/before-after-2021-12-04 13:55:38.212561.model"
    model = word2vec.Word2Vec.load(path)
    similar_words = model.wv.most_similar(positive=["ln"], topn=10)
    for similar_word in similar_words:

        print(similar_word)

def default():
    file_paths = [comp for comp in glob.glob(BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths:
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
        
            context_before = Graph.toContent(contents)
            context_after = Graph.toContentAfter(contents)
            for before, after in zip(context_before, context_after):
                trainings.append(before)
                trainings.append(after)

    W2V.execute(trainings, "default-test")

def default_test():
    path = "libs/delv/default-test-2021-12-05 01:45:27.835636.model"
    model = word2vec.Word2Vec.load(path)
    similar_words = model.wv.most_similar(positive=["apt-get", "install", "update", "-y", "--no-install-recommends"], topn=10)
    for similar_word in similar_words:

        print(similar_word)

def debian_default():
    file_paths = [comp for comp in glob.glob(DEBIAN_BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths:
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
        
            contexts = Graph.toContent(contents)
            for context in contexts:
                trainings.append(context)

    W2V.execute(trainings, "default-test")

def debian_default_test():
    path = "libs/delv/default-test-2021-12-06 01:05:49.243366.model"
    # path = "libs/delv/default-test-2021-12-05 01:45:27.835636.model"
    model = word2vec.Word2Vec.load(path)
    similar_words = model.wv.most_similar(positive=["apt-get", "update", "install"], topn=20)
    for similar_word in similar_words:

        print(similar_word)

def add_test():
    path = "libs/delv/default-test-2021-12-06 01:05:49.243366.model"
    model = word2vec.Word2Vec.load(path)

def cbow():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths:
        model = Model(file_path)
        primitives_key = model.primitives_key
        primitives_dict = model._primitives_dict

        for p_key in primitives_key:
            p_items = primitives_dict[p_key]
            for p_item in p_items:
                tokens = Structure.toToken(p_item)
                tokens = Structure.Equal(tokens)
                # print(tokens)
                trainings.append(tokens)
    
    W2V.cbow(trainings, name="cbow_python_project")

def naive():
    file_paths = [comp for comp in glob.glob(DEBIAN_BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths:
        trainings = []
    for file_path in file_paths:
        model = Dockerfile(file_path)
        primitives_key = model.primitives_key
        primitives_dict = model._primitives_dict

        for p_key in primitives_key:
            p_items = primitives_dict[p_key]
            for p_item in p_items:
                tokens = Structure.toToken(p_item)
                tokens = Structure.Equal(tokens)
                # print(tokens)
                trainings.append(tokens)
    
    W2V.execute(trainings, "naiveDebian")

def naive_test():
    path = "libs/delv/naiveDebian-2021-12-06 03:23:01.259376.model"
    # path = "libs/delv/default-test-2021-12-05 01:45:27.835636.model"
    model = word2vec.Word2Vec.load(path)
    similar_words = model.wv.most_similar(positive=["apt-get", "install"], topn=20)
    for similar_word in similar_words:
        print(similar_word)

def doc2vec_model():
    file_paths = [comp for comp in glob.glob(DEBIAN_BINNACLE_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    trainings = []
    for file_path in file_paths:
        # 
        print()
        primitive = Primitive(file_path)
        # print(primitive.data)
        responses, hash_dict = Structure.toStack(primitive.data)
        for response in responses:
            # contents = []
            for res in response:
                tokens = hash_dict[res]
                tokens = Structure.toToken(tokens)
                tokens = Structure.Equal(tokens)
                trainings.append(tokens)
    
    D2V.execute(trainings, "naiveDebian")

def main():


    test_3()




    

    # test()
    # test_2()




    # test_4()
    # test_4()


    # test_5()
    # test_6()
    # test_7()
    # test_9()
    # test_10()
    # default_test()
    # debian_default_test()
    # naive_test()



if __name__ == "__main__":
    main()
