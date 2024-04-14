from typing import BinaryIO


class Buffer:
    def __init__(self, stream: BinaryIO):
        self.stream = stream

    def read(self, n: int) -> bytes:
        return self.stream.read(n)

    def read_int(self, n: int, is_ms_byte: bool = False) -> int:
        return int.from_bytes(self.read(n), 'big' if is_ms_byte else 'little')

    def read_int8(self) -> int:
        return self.read_int(1)

    def read_int16(self, is_ms_byte: bool = False) -> int:
        return self.read_int(2, is_ms_byte)

    def read_int32(self, is_ms_byte: bool = False) -> int:
        return self.read_int(4, is_ms_byte)

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

    def write_int(self, i: int, n: int, is_ms_byte: bool = False) -> int:
        return self.write(i.to_bytes(n, 'big' if is_ms_byte else 'little'))

    def write_int8(self, i: int) -> int:
        return self.write_int(i, 1)

    def write_int16(self, i: int, is_ms_byte: bool = False) -> int:
        return self.write_int(i, 2, is_ms_byte)

    def write_int32(self, i: int, is_ms_byte: bool = False) -> int:
        return self.write_int(i, 4, is_ms_byte)

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
