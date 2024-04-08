from typing import BinaryIO, Literal

type ByteOrder = Literal['little', 'big']


class Buffer:
    def __init__(self, stream: BinaryIO):
        self.stream = stream

    def seek(self, offset: int):
        self.stream.seek(offset)

    def tell(self) -> int:
        return self.stream.tell()

    def read(self, n: int) -> bytes:
        return self.stream.read(n)

    def skip(self, n: int):
        self.seek(self.tell() + n)

    def read_byte(self) -> bytes:
        return self.read(1)

    def skip_byte(self):
        self.skip(1)

    def read_int(self, byte_order: ByteOrder) -> int:
        return int.from_bytes(self.read(4), byte_order)

    def read_int_le(self) -> int:
        return self.read_int('little')

    def read_int_be(self) -> int:
        return self.read_int('big')

    def skip_int(self):
        self.skip(4)

    def read_until(self, end: bytes) -> bytearray:
        data = bytearray()
        while True:
            b = self.read_byte()
            if b is None or b == end:
                break
            data.extend(b)
        return data
