import string
from pathlib import Path

from utils import MsgType, Logger


class FileValidator:
    def __init__(self, path):
        self.path = path
        self.__chars = set(string.ascii_letters + string.digits)
        self.__id_length = 8
        self.__format = ['.webm', '.webp']

    def has_thumb(self):
        pass

    def has_preview(self):
        pass

    def is_correct_format(self):
        return Path(self.path).suffix in self.__format

    def converted(self):
        stem = Path(self.path).stem
        if self.is_correct_format():
            if len(stem) == self.__id_length and all(char in self.__chars for char in stem):
                return True
        Logger(MsgType.DEBUG, f'File {self.path} has not yet been converted.')
        return False


class DirValidator:
    def __init__(self, path: str):
        self.abs_path = path
        self.__dirs = ['profile', 'thumb', 'preview']

    def uniques(self):
        ids, hits = set(), []
        for folder in Path(self.abs_path).iterdir():
            for file in folder.iterdir():
                if file.is_dir():
                    continue
                file_id = file.stem
                if file_id in ids:
                    hits.append(str(file))
        if hits:
            Logger(MsgType.WARNING, f'Found double ids: {hits}, renaming hits.')
        pass

    def make_dirs(self):
        path = Path(self.abs_path)
        if not path.exists() or path.is_file():
            Logger(MsgType.ERROR, f'Base folder of {path} is non-existent or is a file.')
            return False
        for dirs in path.iterdir():
            if dirs.is_file():
                Logger(MsgType.WARNING, f'Found file in {path}, found: {dirs}. Only expects folders.')
                continue
            for folder in self.__dirs:
                path = dirs.joinpath(folder)
                if path.exists():
                    continue
                path.mkdir(exist_ok=True)
                Logger(MsgType.INFO, f'Created folder {folder} in {path}.')
        return True
