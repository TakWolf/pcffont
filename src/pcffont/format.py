from enum import IntFlag

from pcffont.error import PcfParseError
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer


class PcfTableFormat(IntFlag):
    DEFAULT_FORMAT = 0b_0000_0000_0000
    INKBOUNDS = 0b_0010_0000_0000
    ACCEL_W_INKBOUNDS = 0b_0001_0000_0000
    COMPRESSED_METRICS = 0b_0001_0000_0000

    MASK_GLYPH_PAD = 0b_00_00_11
    MASK_BYTE_ORDER = 0b_00_01_00
    MASK_BIT_ORDER = 0b_00_10_00
    MASK_SCAN_UNIT = 0b_11_00_00

    @staticmethod
    def build(
            ms_byte_first: bool = True,
            ms_bit_first: bool = True,
            has_ink_bounds: bool = False,
            is_compressed_metrics: bool = False,
            glyph_pad_config: int = 2,
            scan_unit_config: int = 0,
    ) -> int:
        table_format = PcfTableFormat.DEFAULT_FORMAT
        if ms_byte_first:
            table_format |= PcfTableFormat.MASK_BYTE_ORDER
        if ms_bit_first:
            table_format |= PcfTableFormat.MASK_BIT_ORDER
        if has_ink_bounds:
            table_format |= PcfTableFormat.ACCEL_W_INKBOUNDS
        if is_compressed_metrics:
            table_format |= PcfTableFormat.COMPRESSED_METRICS
        table_format |= glyph_pad_config
        table_format |= scan_unit_config << 4
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
        return table_format & PcfTableFormat.MASK_BYTE_ORDER > 0

    @staticmethod
    def ms_bit_first(table_format: int) -> bool:
        return table_format & PcfTableFormat.MASK_BIT_ORDER > 0

    @staticmethod
    def has_ink_bounds(table_format: int) -> bool:
        return table_format & PcfTableFormat.ACCEL_W_INKBOUNDS > 0

    @staticmethod
    def is_compressed_metrics(table_format: int) -> bool:
        return table_format & PcfTableFormat.COMPRESSED_METRICS > 0

    @staticmethod
    def glyph_pad_config(table_format: int) -> int:
        """
        The font glyph padding.
        Each glyph in the font will have each scanline padded in to a multiple of n bytes.

        glyph_pad = [1, 2, 4, 8][glyph_pad_config]
        """
        return table_format & PcfTableFormat.MASK_GLYPH_PAD

    @staticmethod
    def scan_unit_config(table_format: int) -> int:
        """
        The font scanline unit.
        When the font bit order is different from the font byte order, the scanline unit n describes
        what unit of data (in bytes) are to be swapped.

        scan_unit = [1, 2, 4][scan_unit_config]
        """
        return (table_format & PcfTableFormat.MASK_SCAN_UNIT) >> 4
