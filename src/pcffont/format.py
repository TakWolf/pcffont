from enum import IntFlag

from pcffont.error import PcfError
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
            is_ms_byte: bool = True,
            is_ms_bit: bool = True,
    ) -> int:
        table_format = PcfTableFormat.DEFAULT_FORMAT
        if is_ms_byte:
            table_format |= PcfTableFormat.MASK_BYTE
        if is_ms_bit:
            table_format |= PcfTableFormat.MASK_BIT
        return table_format

    @staticmethod
    def build_for_accelerators(
            is_ms_byte: bool = True,
            is_ms_bit: bool = True,
            has_ink_bounds: bool = False,
    ) -> int:
        table_format = PcfTableFormat.DEFAULT_FORMAT
        if is_ms_byte:
            table_format |= PcfTableFormat.MASK_BYTE
        if is_ms_bit:
            table_format |= PcfTableFormat.MASK_BIT
        if has_ink_bounds:
            table_format |= PcfTableFormat.ACCEL_W_INKBOUNDS
        return table_format

    @staticmethod
    def build_for_metrics(
            is_ms_byte: bool = True,
            is_ms_bit: bool = True,
            is_compressed: bool = True,
    ) -> int:
        table_format = PcfTableFormat.DEFAULT_FORMAT
        if is_ms_byte:
            table_format |= PcfTableFormat.MASK_BYTE
        if is_ms_bit:
            table_format |= PcfTableFormat.MASK_BIT
        if is_compressed:
            table_format |= PcfTableFormat.COMPRESSED_METRICS
        return table_format

    @staticmethod
    def build_for_bitmaps(
            is_ms_byte: bool = True,
            is_ms_bit: bool = True,
            bitmap_pad_mode: int = 2,
            bit_scan_mode: int = 0,
    ) -> int:
        table_format = PcfTableFormat.DEFAULT_FORMAT
        if is_ms_byte:
            table_format |= PcfTableFormat.MASK_BYTE
        if is_ms_bit:
            table_format |= PcfTableFormat.MASK_BIT
        table_format |= bitmap_pad_mode
        table_format |= bit_scan_mode >> 4
        return table_format

    @staticmethod
    def read_and_check(buffer: Buffer, header: PcfHeader) -> int:
        buffer.seek(header.table_offset)
        table_format = buffer.read_int32()
        if table_format != header.table_format:
            raise PcfError(f"The table format definition is inconsistent with the header: type '{header.table_type.name}', offset {header.table_offset}")
        return table_format

    @staticmethod
    def is_ms_byte(table_format: int) -> bool:
        return table_format & PcfTableFormat.MASK_BYTE > 0

    @staticmethod
    def is_ms_bit(table_format: int) -> bool:
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
