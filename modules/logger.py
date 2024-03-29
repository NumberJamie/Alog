from enum import Enum


class MsgType(Enum):
    INFO = ['\033[92m', '[INFO]']
    WARNING = ['\033[93m', '[WARNING]']
    DEBUG = ['\033[94m', '[DEBUG]']
    ERROR = ['\033[91m', '[ERROR]']


class Logger:
    def __init__(self, msg_type: MsgType, msg: str):
        self.msg_type = msg_type
        self.msg = msg
        self.debug = True
        self.__reset = '\033[0m'
        self.__print()

    def __print(self):
        if not self.debug and self.msg_type == MsgType.DEBUG:
            return
        print(f'{self.msg_type.value[0]}{self.msg_type.value[1]}{self.__reset} {self.msg}')
