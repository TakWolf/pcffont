import os
from typing import BinaryIO


class PcfFont:
    @staticmethod
    def parse(buffer: BinaryIO) -> 'PcfFont':
        # TODO
        pass

    @staticmethod
    def load(file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> 'PcfFont':
        with open(file_path, 'rb') as file:
            return PcfFont.parse(file)

    def __init__(self):
        # TODO
        pass

    def dump(self, buffer: BinaryIO):
        # TODO
        pass

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        with open(file_path, 'wb') as file:
            self.dump(file)
