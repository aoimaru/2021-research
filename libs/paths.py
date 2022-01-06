import pathlib
import glob


class Path(object):
    @staticmethod
    def get_file_path(PROJECT_PATH):
        file_paths = []
        temp = pathlib.Path(PROJECT_PATH)
        for comp in temp.glob("**/*.json"):
            ph = pathlib.Path(comp)
            abs_path = pathlib.Path(ph.resolve())
            file_paths.append(abs_path)
        return file_paths










