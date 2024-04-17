from enum import IntEnum

from pcffont.error import PcfParseError
from pcffont.internal.buffer import Buffer

_FILE_VERSION = b'\x01fcp'


class PcfTableType(IntEnum):
    PROPERTIES = 1 << 0
    ACCELERATORS = 1 << 1
    METRICS = 1 << 2
    BITMAPS = 1 << 3
    INK_METRICS = 1 << 4
    BDF_ENCODINGS = 1 << 5
    SWIDTHS = 1 << 6
    GLYPH_NAMES = 1 << 7
    BDF_ACCELERATORS = 1 << 8


class PcfHeader:
    @staticmethod
    def parse(buffer: Buffer) -> list['PcfHeader']:
        buffer.seek(0)
        if buffer.read(4) != _FILE_VERSION:
            raise PcfParseError('Not PCF format')

        tables_count = buffer.read_uint32()

        headers = []
        for _ in range(tables_count):
            table_type = PcfTableType(buffer.read_uint32())
            table_format = buffer.read_uint32()
            table_size = buffer.read_uint32()
            table_offset = buffer.read_uint32()
            headers.append(PcfHeader(table_type, table_format, table_size, table_offset))

        return headers

    @staticmethod
    def dump(buffer: Buffer, headers: list['PcfHeader']):
        buffer.seek(0)
        buffer.write(_FILE_VERSION)

        buffer.write_uint32(len(headers))
        for header in headers:
            buffer.write_uint32(header.table_type)
            buffer.write_uint32(header.table_format)
            buffer.write_uint32(header.table_size)
            buffer.write_uint32(header.table_offset)

    def __init__(self, table_type: PcfTableType, table_format: int, table_size: int, table_offset: int):
        self.table_type = table_type
        self.table_format = table_format
        self.table_size = table_size
        self.table_offset = table_offset
