from lib.dockerfiles import Dockerfile
from lib.primitives import Primitive
from lib.structures import Structure
 

TEST_PATH = "./python/3.6/alpine3.13/Dockerfile"

def test():
    # df = Dockerfile(TEST_PATH)
    primitive = Primitive(TEST_PATH)
    data = primitive.data
    Structure.toJson(data)
    
    




def main():
    test()

if __name__ == "__main__":
    main()