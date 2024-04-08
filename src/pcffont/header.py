from enum import IntEnum, IntFlag

from pcffont.error import PcfError
from pcffont.internal.stream import Buffer


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


class PcfTableFormat(IntFlag):
    DEFAULT_FORMAT = 0b_0000_0000_0000
    INKBOUNDS = 0b_0010_0000_0000
    ACCEL_W_INKBOUNDS = 0b_0001_0000_0000
    COMPRESSED_METRICS = 0b_0001_0000_0000


class PcfTableFormatMask(IntFlag):
    GLYPH_PAD = 0b_0000_0011
    BYTE = 0b_0000_0100
    BIT = 0b_0000_1000
    SCAN_UNIT = 0b_0011_0000


class PcfHeader:
    @staticmethod
    def parse(buffer: Buffer) -> list['PcfHeader']:
        if buffer.read(4) != b'\x01fcp':
            raise PcfError('Not PCF format')

        tables_count = buffer.read_int_le()

        headers = []
        for _ in range(tables_count):
            table_type = PcfTableType(buffer.read_int_le())
            table_format = buffer.read_int_le()
            size = buffer.read_int_le()
            offset = buffer.read_int_le()
            headers.append(PcfHeader(table_type, table_format, size, offset))
        return headers

    def __init__(self, table_type: PcfTableType, table_format: int, size: int, offset: int):
        self.table_type = table_type
        self.table_format = table_format
        self.size = size
        self.offset = offset
