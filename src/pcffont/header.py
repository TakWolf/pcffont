from enum import IntEnum, IntFlag

from pcffont.error import PcfError
from pcffont.internal.stream import ByteOrder, Buffer


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
    def parse(buffer: Buffer) -> dict[PcfTableType, 'PcfHeader']:
        tables_count = buffer.read_int32_le()

        headers = {}
        for _ in range(tables_count):
            table_type = PcfTableType(buffer.read_int32_le())
            table_format = buffer.read_int32_le()
            table_size = buffer.read_int32_le()
            table_offset = buffer.read_int32_le()

            if table_type in headers:
                raise PcfError(f"Duplicate table '{table_type.name}'")
            headers[table_type] = PcfHeader(table_type, table_format, table_size, table_offset)

        return headers

    def __init__(self, table_type: PcfTableType, table_format: int, table_size: int, table_offset: int):
        self.table_type = table_type
        self.table_format = table_format
        self.table_size = table_size
        self.table_offset = table_offset

    def get_and_check_table_format(self, buffer: Buffer) -> tuple[int, ByteOrder]:
        buffer.seek(self.table_offset)
        table_format = buffer.read_int32_le()
        if table_format != self.table_format:
            raise PcfError(f"The table format definition is inconsistent with the header: type '{self.table_type.name}', offset {self.table_offset}")

        byte_order: ByteOrder = 'little'
        if table_format & (PcfTableFormatMask.BYTE | PcfTableFormatMask.BIT) > 0:
            byte_order = 'big'

        return table_format, byte_order

    def dump(self, buffer: Buffer):
        buffer.write_int32_le(self.table_type)
        buffer.write_int32_le(self.table_format)
        buffer.write_int32_le(self.table_size)
        buffer.write_int32_le(self.table_offset)
