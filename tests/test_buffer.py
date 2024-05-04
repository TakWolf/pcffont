import random
from io import BytesIO

from pcffont.internal.buffer import Buffer


def test_byte():
    buffer = Buffer(BytesIO())
    size = 0
    size += buffer.write(b'Hello World')
    size += buffer.write_nulls(4)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read(11) == b'Hello World'
    assert buffer.read(4) == b'\x00\x00\x00\x00'
    assert buffer.tell() == size


def test_int8():
    data = [random.randint(-0x80, 0x7F) for _ in range(20)]

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_int8(value)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_int8_list(len(data)) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_int8_list(data)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_int8() == value
    assert buffer.tell() == size


def test_uint8():
    data = [random.randint(0, 0xFF) for _ in range(20)]

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_uint8(value)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_uint8_list(len(data)) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_uint8_list(data)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_uint8() == value
    assert buffer.tell() == size


def test_int16():
    data = [random.randint(-0x80_00, 0x7F_FF) for _ in range(20)]

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_int16(value, True)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_int16_list(len(data), True) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_int16_list(data, True)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_int16(True) == value
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_int16(value, False)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_int16_list(len(data), False) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_int16_list(data, False)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_int16(False) == value
    assert buffer.tell() == size


def test_uint16():
    data = [random.randint(0, 0xFF_FF) for _ in range(20)]

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_uint16(value, True)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_uint16_list(len(data), True) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_uint16_list(data, True)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_uint16(True) == value
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_uint16(value, False)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_uint16_list(len(data), False) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_uint16_list(data, False)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_uint16(False) == value
    assert buffer.tell() == size


def test_int32():
    data = [random.randint(-0x80_00_00_00, 0x7F_FF_FF_FF) for _ in range(20)]

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_int32(value, True)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_int32_list(len(data), True) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_int32_list(data, True)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_int32(True) == value
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_int32(value, False)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_int32_list(len(data), False) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_int32_list(data, False)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_int32(False) == value
    assert buffer.tell() == size


def test_uint32():
    data = [random.randint(0, 0xFF_FF_FF_FF) for _ in range(20)]

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_uint32(value, True)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_uint32_list(len(data), True) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_uint32_list(data, True)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_uint32(True) == value
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_uint32(value, False)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_uint32_list(len(data), False) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_uint32_list(data, False)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_uint32(False) == value
    assert buffer.tell() == size


def test_binary():
    buffer = Buffer(BytesIO())
    size = 0
    size += buffer.write_binary([1, 1, 1, 1, 0, 0, 0, 0], True)
    size += buffer.write_binary([1, 1, 1, 1, 0, 0, 0, 0], False)
    size += buffer.write_binary_list([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ], True)
    size += buffer.write_binary_list([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ], False)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_binary(True) == [1, 1, 1, 1, 0, 0, 0, 0]
    assert buffer.read_binary(False) == [1, 1, 1, 1, 0, 0, 0, 0]
    assert buffer.read_binary_list(2, True) == [
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ]
    assert buffer.read_binary_list(2, False) == [
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
    ]
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_binary(False) == [0, 0, 0, 0, 1, 1, 1, 1]
    assert buffer.read_binary(True) == [0, 0, 0, 0, 1, 1, 1, 1]
    assert buffer.read_binary_list(2, False) == [
        [0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0],
    ]
    assert buffer.read_binary_list(2, True) == [
        [0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0],
    ]
    assert buffer.tell() == size


def test_string():
    data = ['ABC', 'DEF', '12345', '67890']

    buffer = Buffer(BytesIO())
    size = 0
    for value in data:
        size += buffer.write_string(value)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_string_list(len(data)) == data
    assert buffer.tell() == size

    buffer = Buffer(BytesIO())
    size = buffer.write_string_list(data)
    assert buffer.tell() == size
    buffer.seek(0)
    for value in data:
        assert buffer.read_string() == value
    assert buffer.tell() == size


def test_bool():
    buffer = Buffer(BytesIO())
    size = 0
    size += buffer.write_bool(True)
    size += buffer.write_bool(False)
    assert buffer.tell() == size
    buffer.seek(0)
    assert buffer.read_bool()
    assert not buffer.read_bool()
    assert buffer.tell() == size


def test_skip():
    buffer = Buffer(BytesIO())
    buffer.write_nulls(100)
    assert buffer.tell() == 100
    buffer.seek(25)
    buffer.skip(50)
    assert buffer.tell() == 75
