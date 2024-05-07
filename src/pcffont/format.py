from typing import Any

_DEFAULT_FORMAT = 0b_0000_0000_0000
_ACCEL_W_INKBOUNDS_OR_COMPRESSED_METRICS = 0b_0001_0000_0000

_MASK_GLYPH_PAD = 0b_00_00_11
_MASK_BYTE_ORDER = 0b_00_01_00
_MASK_BIT_ORDER = 0b_00_10_00
_MASK_SCAN_UNIT = 0b_11_00_00


class PcfTableFormat:
    @staticmethod
    def parse(value: int) -> 'PcfTableFormat':
        ms_byte_first = value & _MASK_BYTE_ORDER > 0
        ms_bit_first = value & _MASK_BIT_ORDER > 0
        ink_or_compressed_metrics = value & _ACCEL_W_INKBOUNDS_OR_COMPRESSED_METRICS > 0
        glyph_pad_index = value & _MASK_GLYPH_PAD
        scan_unit_index = (value & _MASK_SCAN_UNIT) >> 4
        return PcfTableFormat(
            ms_byte_first,
            ms_bit_first,
            ink_or_compressed_metrics,
            glyph_pad_index,
            scan_unit_index,
        )

    def __init__(
            self,
            ms_byte_first: bool = True,
            ms_bit_first: bool = True,
            ink_or_compressed_metrics: bool = False,
            glyph_pad_index: int = 0,
            scan_unit_index: int = 0,
    ):
        """
        :param ms_byte_first:
            If true, sets the font byte order to MSB first.
            All multi-byte data in the file (metrics, bitmaps and everything else) will be written most significant
            byte first.
        :param ms_bit_first:
            If true, sets the font bit order to MSB first.
            Bits for each glyph will be placed in this order; i.e., the left most bit on the screen will be in the
            highest valued bit in each unit.
        :param ink_or_compressed_metrics:
            If true, the `PcfAccelerators` will include the `ink_min_bounds` and `ink_max_bounds` fields,
            or the `PcfMetrics` will be compressed.
        :param glyph_pad_index:
            The font glyph padding. Each glyph in the font will have each scanline padded in to a multiple of n bytes.
            glyph_pad = [1, 2, 4, 8][glyph_pad_index]
        :param scan_unit_index:
            The font scanline unit. When the font bit order is different from the font byte order, the scanline unit
            n describes what unit of data (in bytes) are to be swapped.
            scan_unit = [1, 2, 4, 8][scan_unit_index]
        """
        self.ms_byte_first = ms_byte_first
        self.ms_bit_first = ms_bit_first
        self.ink_or_compressed_metrics = ink_or_compressed_metrics
        self.glyph_pad_index = glyph_pad_index
        self.scan_unit_index = scan_unit_index

    def __repr__(self) -> str:
        value = self.value
        return f'{value}#{value:010b}'

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfTableFormat):
            return False
        return (self.ms_byte_first == other.ms_byte_first and
                self.ms_bit_first == other.ms_bit_first and
                self.ink_or_compressed_metrics == other.ink_or_compressed_metrics and
                self.glyph_pad_index == other.glyph_pad_index and
                self.scan_unit_index == other.scan_unit_index)

    @property
    def value(self) -> int:
        value = _DEFAULT_FORMAT
        if self.ms_byte_first:
            value |= _MASK_BYTE_ORDER
        if self.ms_bit_first:
            value |= _MASK_BIT_ORDER
        if self.ink_or_compressed_metrics:
            value |= _ACCEL_W_INKBOUNDS_OR_COMPRESSED_METRICS
        value |= self.glyph_pad_index
        value |= self.scan_unit_index << 4
        return value
