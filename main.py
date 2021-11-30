import glob
import os

from libs.dockerfiles import Dockerfile
from libs.primitives import Primitive
from libs.structures import Structure
 

GOLANG_PROJECT = "./golang/**"

def test():
    # df = Dockerfile(TEST_PATH)
    file_paths = [comp for comp in glob.glob(GOLANG_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths:
        primitive = Primitive(file_path)
        data = primitive.data
        layers, hash_dict = Structure.toStack(data)
        for layer in layers:
            print()
            comps = [hash_dict[comp] for comp in layer]
            for comp in comps:
                print(comp)




def main():
    test()

if __name__ == "__main__":
    main()