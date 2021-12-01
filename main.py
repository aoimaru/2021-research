import glob
import os

from libs.dockerfiles import Model
from libs.primitives import Primitive
from libs.structures import Structure
 

PYTHON_PROJECT = "./python/**"
OTHERS_PROJECT = "./Others/**"

def test():
    # df = Dockerfile(TEST_PATH)
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths:
        print()
        primitive = Primitive(file_path)
        responses, hash_dict = Structure.toStack(primitive.data)
        for response in responses:
            print()

            for res in response:
                tokens = hash_dict[res]
                tokens = Structure.And(tokens)
                tokens = Structure.toToken(tokens)

        





def test_2():
    pass


def main():

    test()
    test_2()

if __name__ == "__main__":
    main()