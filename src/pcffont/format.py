from enum import IntFlag

from pcffont.error import PcfParseError
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer


class PcfTableFormat(IntFlag):
    DEFAULT_FORMAT = 0b_0000_0000_0000
    INKBOUNDS = 0b_0010_0000_0000
    ACCEL_W_INKBOUNDS = 0b_0001_0000_0000
    COMPRESSED_METRICS = 0b_0001_0000_0000

    MASK_BYTE = 0b_0000_0100
    MASK_BIT = 0b_0000_1000
    MASK_GLYPH_PAD = 0b_0000_0011
    MASK_SCAN_UNIT = 0b_0011_0000

    @staticmethod
    def build(
            ms_byte_first: bool = True,
            ms_bit_first: bool = True,
            bitmap_pad_mode: int = 2,
            bit_scan_mode: int = 0,
            has_ink_bounds: bool = False,
            is_compressed_metrics: bool = False,
    ) -> int:
        table_format = PcfTableFormat.DEFAULT_FORMAT
        if ms_byte_first:
            table_format |= PcfTableFormat.MASK_BYTE
        if ms_bit_first:
            table_format |= PcfTableFormat.MASK_BIT
        table_format |= bitmap_pad_mode
        table_format |= bit_scan_mode >> 4
        if has_ink_bounds:
            table_format |= PcfTableFormat.ACCEL_W_INKBOUNDS
        if is_compressed_metrics:
            table_format |= PcfTableFormat.COMPRESSED_METRICS
        return table_format

    @staticmethod
    def read_and_check(buffer: Buffer, header: PcfHeader) -> int:
        buffer.seek(header.table_offset)
        table_format = buffer.read_uint32()
        if table_format != header.table_format:
            raise PcfParseError(f"The table format definition is inconsistent with the header: type '{header.table_type.name}', offset {header.table_offset}")
        return table_format

    @staticmethod
    def ms_byte_first(table_format: int) -> bool:
        return table_format & PcfTableFormat.MASK_BYTE > 0

    @staticmethod
    def ms_bit_first(table_format: int) -> bool:
        return table_format & PcfTableFormat.MASK_BIT > 0

    @staticmethod
    def has_ink_bounds(table_format: int) -> bool:
        return table_format & PcfTableFormat.ACCEL_W_INKBOUNDS > 0

    @staticmethod
    def is_compressed_metrics(table_format: int) -> bool:
        return table_format & PcfTableFormat.COMPRESSED_METRICS > 0

    @staticmethod
    def bitmap_pad_mode(table_format: int) -> int:
        """
        How each row in each glyph's bitmap is padded
        :return: 0 => byte, 1 => short, 2 => int32, 3 => int64
        """
        return table_format & PcfTableFormat.MASK_GLYPH_PAD

    @staticmethod
    def bit_scan_mode(table_format: int) -> int:
        """
        Bitmap scan unit
        :return: 0 => byte, 1 => short, 2 => int32
        """
        return table_format & PcfTableFormat.MASK_SCAN_UNIT
