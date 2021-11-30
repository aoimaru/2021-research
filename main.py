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
        runs = model.runs
        for run in runs:
            cnt = []
            for shells in run:
                while shells:
                    word = shells.pop(0)
                    if not word:
                        continue
                    if word == "NL":
                        continue
                    if word == "SPACE":
                        continue
                    cnt.append(word)
            print()
            print(cnt)






def main():
    test()

if __name__ == "__main__":
    main()