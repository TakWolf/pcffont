from typing import BinaryIO, Literal

type ByteOrder = Literal['little', 'big']


def read_int32(buffer: BinaryIO, byte_order: ByteOrder) -> int:
    return int.from_bytes(buffer.read(4), byte_order)


def read_int32_le(buffer: BinaryIO) -> int:
    return read_int32(buffer, 'little')


def read_int32_be(buffer: BinaryIO) -> int:
    return read_int32(buffer, 'big')
