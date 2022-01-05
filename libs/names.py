import os
import re

class Name(object):
    @staticmethod
    def file_path_to_name(file_path):
        file_name = os.path.basename(file_path)
        file_name = re.sub(".Dockerfile", "", file_name)
        return file_name
