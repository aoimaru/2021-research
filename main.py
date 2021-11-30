import glob
import os

from libs.dockerfiles import Model
from libs.primitives import Primitive
from libs.structures import Structure
 

PYTHON_PROJECT = "./python/**"

def test():
    # df = Dockerfile(TEST_PATH)
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths:
        model = Model(file_path)
        commands = model.commands
        for command in commands:
            print(command)





def main():
    test()

if __name__ == "__main__":
    main()