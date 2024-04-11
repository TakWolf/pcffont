from typing import BinaryIO, Literal, TypeAlias

# TODO # type ByteOrder = Literal['little', 'big']
ByteOrder: TypeAlias = Literal['little', 'big']


class Buffer:
    def __init__(self, stream: BinaryIO):
        self.stream = stream

    def read(self, n: int) -> bytes:
        return self.stream.read(n)

    def read_int(self, n: int, byte_order: ByteOrder) -> int:
        return int.from_bytes(self.read(n), byte_order)

    def read_int_le(self, n: int) -> int:
        return self.read_int(n, 'little')

    def read_int_be(self, n: int) -> int:
        return self.read_int(n, 'big')

    def read_int32(self, byte_order: ByteOrder) -> int:
        return self.read_int(4, byte_order)

    def read_int32_le(self) -> int:
        return self.read_int32('little')

    def read_int32_be(self) -> int:
        return self.read_int32('big')

    def read_int16(self, byte_order: ByteOrder) -> int:
        return self.read_int(2, byte_order)

    def read_int16_le(self) -> int:
        return self.read_int16('little')

    def read_int16_be(self) -> int:
        return self.read_int16('big')

    def read_int8(self, byte_order: ByteOrder) -> int:
        return self.read_int(1, byte_order)

    def read_int8_le(self) -> int:
        return self.read_int8('little')

    def read_int8_be(self) -> int:
        return self.read_int8('big')

    def read_bool(self) -> bool:
        return self.read(1) != b'\x00'

    def read_string(self) -> str:
        data = bytearray()
        while True:
            b = self.read(1)
            if b == b'\x00' or b == b'':
                break
            data.extend(b)
        return data.decode('utf-8')

    def write(self, s: bytes) -> int:
        return self.stream.write(s)

    def write_int(self, i: int, n: int, byte_order: ByteOrder) -> int:
        return self.write(i.to_bytes(n, byte_order))

    def write_int_le(self, i: int, n: int) -> int:
        return self.write_int(i, n, 'little')

    def write_int_be(self, i: int, n: int) -> int:
        return self.write_int(i, n, 'big')

    def write_int32(self, i: int, byte_order: ByteOrder) -> int:
        return self.write_int(i, 4, byte_order)

    def write_int32_le(self, i: int) -> int:
        return self.write_int32(i, 'little')

    def write_int32_be(self, i: int) -> int:
        return self.write_int32(i, 'big')

    def write_int16(self, i: int, byte_order: ByteOrder) -> int:
        return self.write_int(i, 2, byte_order)

    def write_int16_le(self, i: int) -> int:
        return self.write_int16(i, 'little')

    def write_int16_be(self, i: int) -> int:
        return self.write_int16(i, 'big')

    def write_int8(self, i: int, byte_order: ByteOrder) -> int:
        return self.write_int(i, 1, byte_order)

    def write_int8_le(self, i: int) -> int:
        return self.write_int8(i, 'little')

    def write_int8_be(self, i: int) -> int:
        return self.write_int8(i, 'big')

    def write_bool(self, b: bool) -> int:
        return self.write(b'\x01' if b else b'\x00')

    def write_nulls(self, n: int) -> int:
        for _ in range(n):
            self.write(b'\x00')
        return n

    def write_string(self, s: str) -> int:
        return self.write(s.encode('utf-8')) + self.write_nulls(1)

    def skip(self, n: int):
        self.seek(self.tell() + n)

    def skip_int(self):
        self.skip(4)

    def seek(self, offset: int):
        self.stream.seek(offset)

    def tell(self) -> int:
        return self.stream.tell()
