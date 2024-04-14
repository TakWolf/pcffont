from enum import IntFlag


class PcfTableFormat(IntFlag):
    DEFAULT_FORMAT = 0b_0000_0000_0000
    INKBOUNDS = 0b_0010_0000_0000
    ACCEL_W_INKBOUNDS = 0b_0001_0000_0000
    COMPRESSED_METRICS = 0b_0001_0000_0000


class PcfTableFormatMask(IntFlag):
    BYTE = 0b_0000_0100
    BIT = 0b_0000_1000
    GLYPH_PAD = 0b_0000_0011
    SCAN_UNIT = 0b_0011_0000
