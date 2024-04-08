from typing import BinaryIO, Literal

type ByteOrder = Literal['little', 'big']


class Buffer:
    def __init__(self, stream: BinaryIO):
        self.stream = stream

    def read(self, n: int) -> bytes:
        return self.stream.read(n)

    def read_int(self, byte_order: ByteOrder) -> int:
        return int.from_bytes(self.read(4), byte_order)

    def read_int_le(self) -> int:
        return self.read_int('little')

    def read_int_be(self) -> int:
        return self.read_int('big')

    def read_until(self, end: bytes) -> bytearray:
        data = bytearray()
        while True:
            b = self.read(1)
            if b is None or b == end:
                break
            data.extend(b)
        return data

    def write(self, s: bytes) -> int:
        return self.stream.write(s)

    def write_int(self, i: int, byte_order: ByteOrder) -> int:
        return self.write(i.to_bytes(4, byte_order))

    def write_int_le(self, i: int) -> int:
        return self.write_int(i, 'little')

    def write_int_be(self, i: int) -> int:
        return self.write_int(i, 'big')

    def write_by_null(self, n: int) -> int:
        for _ in range(n):
            self.write(b'\x00')
        return n

    def skip(self, n: int):
        self.seek(self.tell() + n)

    def skip_int(self):
        self.skip(4)

    def seek(self, offset: int):
        self.stream.seek(offset)

    def tell(self) -> int:
        return self.stream.tell()
