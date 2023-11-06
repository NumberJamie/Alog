import random
import string
from pathlib import Path

from filetype import is_video, is_image

from modules import Logger, MsgType


class Id:
    def __init__(self):
        self.__id_size = 8
        self.__chars = string.ascii_letters + string.digits
        self.__special = ['avatar', 'header']

    def generate(self):
        return ''.join(random.choices(self.__chars, k=8))

    def is_special(self, file_id):
        return file_id in self.__special

    def is_valid(self, file_id):
        if len(file_id) == self.__id_size and all(char in self.__chars for char in file_id):
            return True
        Logger(MsgType.DEBUG, f'Invalid id found: {file_id}')
        return False


class OwnedDirs:
    def __init__(self, path):
        self.path = Path(path)
        self.__dirs = ['profile', 'thumb', 'preview']

    def get_owner(self):
        return self.path.parent

    def get_id_set(self):
        # Not needed?
        ids = set()
        for file in self.path.iterdir():
            if file.is_dir():
                continue
            ids.add(file.stem)
        return ids

    def create(self):
        for folder in self.__dirs:
            path = self.path.joinpath(folder)
            if path.exists():
                continue
            path.mkdir(exist_ok=True)
            Logger(MsgType.INFO, f'Created folder {folder} in {path}.')


class Format:
    def __init__(self, path):
        self.path = Path(path)
        self.__suffix = '.webp'
        self.__format = ['.webm', '.webp']

    def __insert(self, folder):
        return Path(self.path.parent).joinpath(folder).joinpath(self.path.name).with_suffix(self.__suffix)

    def is_web_format(self):
        return Path(self.path).suffix in self.__format

    def is_video_format(self):
        return True if is_video(str(self.path)) else False

    def with_suffix(self, suffix):
        return self.path.with_suffix(suffix)

    def is_image_format(self):
        return True if is_image(str(self.path)) else False

    def get_in_folder(self, folder):
        return self.__insert(folder)

    def is_in_folder(self, folder):
        thumb_path = self.__insert(folder)
        return Path(thumb_path).exists()
