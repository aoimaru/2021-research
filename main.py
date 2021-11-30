from libs.dockerfiles import Dockerfile
from libs.primitives import Primitive
from libs.structures import Structure
 

TEST_PATH = "./python/3.7/alpine3.13/Dockerfile"
TEST_PATH = "./python/3.7/bullseye/slim/Dockerfile"

def test():
    # df = Dockerfile(TEST_PATH)
    primitive = Primitive(TEST_PATH)
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