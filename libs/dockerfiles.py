import dockerfile
import re

class Dockerfile(object):
    def __init__(self, file_path):
        self._contents = dockerfile.parse_file(file_path)
    

    @property
    def contents(self):
        return self._contents
    