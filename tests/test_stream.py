import random
from io import BytesIO

import pytest

from pcffont.internal.stream import Stream


def test_byte():
    stream = Stream(BytesIO())
    size = 0
    size += stream.write(b'Hello World')
    size += stream.write_nulls(4)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read(11) == b'Hello World'
    assert stream.read(4) == b'\x00\x00\x00\x00'
    assert stream.tell() == size


def test_eof():
    stream = Stream(BytesIO())
    with pytest.raises(EOFError):
        stream.read(1)
    stream.read(1, ignore_eof=True)


def test_int8():
    values = [random.randint(-0x80, 0x7F) for _ in range(20)]

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_int8(value)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_int8_list(len(values)) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_int8_list(values)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int8() == value
    assert stream.tell() == size


def test_uint8():
    values = [random.randint(0, 0xFF) for _ in range(20)]

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_uint8(value)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_uint8_list(len(values)) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_uint8_list(values)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint8() == value
    assert stream.tell() == size


def test_int16():
    values = [random.randint(-0x80_00, 0x7F_FF) for _ in range(20)]

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_int16(value, True)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_int16_list(len(values), True) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_int16_list(values, True)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int16(True) == value
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_int16(value, False)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_int16_list(len(values), False) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_int16_list(values, False)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int16(False) == value
    assert stream.tell() == size


def test_uint16():
    values = [random.randint(0, 0xFF_FF) for _ in range(20)]

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_uint16(value, True)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_uint16_list(len(values), True) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_uint16_list(values, True)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint16(True) == value
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_uint16(value, False)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_uint16_list(len(values), False) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_uint16_list(values, False)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint16(False) == value
    assert stream.tell() == size


def test_int32():
    values = [random.randint(-0x80_00_00_00, 0x7F_FF_FF_FF) for _ in range(20)]

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_int32(value, True)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_int32_list(len(values), True) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_int32_list(values, True)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int32(True) == value
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_int32(value, False)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_int32_list(len(values), False) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_int32_list(values, False)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int32(False) == value
    assert stream.tell() == size


def test_uint32():
    values = [random.randint(0, 0xFF_FF_FF_FF) for _ in range(20)]

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_uint32(value, True)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_uint32_list(len(values), True) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_uint32_list(values, True)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint32(True) == value
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_uint32(value, False)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_uint32_list(len(values), False) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_uint32_list(values, False)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint32(False) == value
    assert stream.tell() == size


def test_binary():
    stream = Stream(BytesIO())
    size = 0
    size += stream.write_binary([1, 1, 1, 1, 0, 0, 0, 0], True)
    size += stream.write_binary([1, 1, 1, 1, 0, 0, 0, 0], False)
    size += stream.write_binary_list([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ], True)
    size += stream.write_binary_list([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ], False)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_binary(True) == [1, 1, 1, 1, 0, 0, 0, 0]
    assert stream.read_binary(False) == [1, 1, 1, 1, 0, 0, 0, 0]
    assert stream.read_binary_list(2, True) == [
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ]
    assert stream.read_binary_list(2, False) == [
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ]
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_binary(False) == [0, 0, 0, 0, 1, 1, 1, 1]
    assert stream.read_binary(True) == [0, 0, 0, 0, 1, 1, 1, 1]
    assert stream.read_binary_list(2, False) == [
        [0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0],
    ]
    assert stream.read_binary_list(2, True) == [
        [0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0],
    ]
    assert stream.tell() == size


def test_string():
    values = ['ABC', 'DEF', '12345', '67890']

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_string(value)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_string_list(len(values)) == values
    assert stream.tell() == size

    stream = Stream(BytesIO())
    size = stream.write_string_list(values)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_string() == value
    assert stream.tell() == size


def test_bool():
    stream = Stream(BytesIO())
    size = 0
    size += stream.write_bool(True)
    size += stream.write_bool(False)
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_bool()
    assert not stream.read_bool()
    assert stream.tell() == size


def test_skip():
    stream = Stream(BytesIO())
    stream.write_nulls(100)
    assert stream.tell() == 100
    stream.seek(25)
    stream.skip(50)
    assert stream.tell() == 75


def test_align_to_bit32():
    stream = Stream(BytesIO())
    stream.write(b'abc')
    stream.align_to_bit32_with_nulls()
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read(4) == b'abc\x00'
