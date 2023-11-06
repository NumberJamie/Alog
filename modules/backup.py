from pathlib import Path

from modules import Format, Id, Logger, MsgType


class Backup:
    def __init__(self, path):
        self.path = Path(path)
        self.__save_loc = 'backup.txt'

    def initialize(self):
        if self.read():
            return self.read()
        id_set = set()
        for folder in self.path.iterdir():
            for file in folder.iterdir():
                if not Format(file).is_web_format() or not Id().is_valid(file.stem):
                    continue
                if not Format(file).is_in_folder('thumb'):
                    continue
                if file.suffix == '.webm' and not Format(file).is_in_folder('preview'):
                    continue
                id_set.add(file.stem)
        self.write(id_set)
        Logger(MsgType.INFO, 'Finished initializing backup')
        return id_set

    def read(self):
        if not Path(self.__save_loc).exists():
            return set()
        with open(self.__save_loc, 'r') as file:
            return set(file.read().splitlines())

    def write(self, id_set):
        open(self.__save_loc, 'w').write('\n'.join(id_set))