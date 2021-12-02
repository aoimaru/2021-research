import glob
import os

from libs.dockerfiles import Model
from libs.primitives import Primitive
from libs.structures import Structure
 

PYTHON_PROJECT = "./python/**"
OTHERS_PROJECT = "./Others/**"
GOLANG_PROJECT = "./golang/**"
BINNACLE_PROJECT = "./binnacle-icse2020/**"

def test():
    # df = Dockerfile(TEST_PATH)
    file_paths = [comp for comp in glob.glob(GOLANG_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths[:1]:
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


        










def test_2():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths:
        print()
        model = Model(file_path)
        primitives = model.primitives
        for primitive in primitives:
            print(primitive)




def main():

    test()
    # test_2()

if __name__ == "__main__":
    main()