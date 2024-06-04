import math
from collections import UserList
from typing import Any, Final

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer


def _swap_fragments(fragments: list[list[int]], scan_unit: int):
    if scan_unit == 2:
        for i in range(0, len(fragments), 2):
            fragments[i], fragments[i + 1] = fragments[i + 1], fragments[i]
    elif scan_unit == 4:
        for i in range(0, len(fragments), 4):
            fragments[i], fragments[i + 1], fragments[i + 2], fragments[i + 3] = fragments[i + 3], fragments[i + 2], fragments[i + 1], fragments[i]


class PcfBitmaps(UserList[list[list[int]]]):
    GLYPH_PAD_OPTIONS: Final[list[int]] = [1, 2, 4, 8]
    SCAN_UNIT_OPTIONS: Final[list[int]] = [1, 2, 4, 8]

    @staticmethod
    def parse(buffer: Buffer, font: 'pcffont.PcfFont', header: PcfHeader, strict_level: int) -> 'PcfBitmaps':
        table_format = header.read_and_check_table_format(buffer, strict_level)

        glyph_pad = PcfBitmaps.GLYPH_PAD_OPTIONS[table_format.glyph_pad_index]
        scan_unit = PcfBitmaps.SCAN_UNIT_OPTIONS[table_format.scan_unit_index]

        glyphs_count = buffer.read_uint32(table_format.ms_byte_first)
        bitmap_offsets = buffer.read_uint32_list(glyphs_count, table_format.ms_byte_first)
        bitmaps_sizes = buffer.read_uint32_list(4, table_format.ms_byte_first)
        bitmaps_start = buffer.tell()

        bitmaps = PcfBitmaps(table_format)
        for glyph_index, bitmap_offset in enumerate(bitmap_offsets):
            buffer.seek(bitmaps_start + bitmap_offset)
            metric = font.metrics[glyph_index]
            glyph_row_pad = math.ceil(metric.width / (glyph_pad * 8)) * glyph_pad

            fragments = buffer.read_binary_list(glyph_row_pad * metric.height, table_format.ms_bit_first)
            if table_format.ms_byte_first != table_format.ms_bit_first:
                _swap_fragments(fragments, scan_unit)

            bitmap = []
            for _ in range(metric.height):
                bitmap_row = []
                for _ in range(glyph_row_pad):
                    bitmap_row.extend(fragments.pop(0))
                bitmap_row = bitmap_row[:metric.width]
                bitmap.append(bitmap_row)
            bitmaps.append(bitmap)

        # Compat
        bitmaps._compat_info = bitmaps_sizes

        return bitmaps

    table_format: PcfTableFormat
    _compat_info: list[int] | None

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            bitmaps: list[list[list[int]]] | None = None,
    ):
        super().__init__(bitmaps)
        if table_format is None:
            table_format = PcfTableFormat()
        self.table_format = table_format
        self._compat_info = None

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfBitmaps):
            return False
        return (self.table_format == other.table_format and
                self._compat_info == other._compat_info and
                super().__eq__(other))

    def dump(self, buffer: Buffer, font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyph_pad = PcfBitmaps.GLYPH_PAD_OPTIONS[self.table_format.glyph_pad_index]
        scan_unit = PcfBitmaps.SCAN_UNIT_OPTIONS[self.table_format.scan_unit_index]

        glyphs_count = len(self)

        bitmaps_start = table_offset + 4 + 4 + 4 * glyphs_count + 4 * 4
        bitmaps_size = 0
        bitmap_offsets = []
        buffer.seek(bitmaps_start)
        for glyph_index, bitmap in enumerate(self):
            bitmap_offsets.append(bitmaps_size)
            metric = font.metrics[glyph_index]
            bitmap_row_width = math.ceil(metric.width / (glyph_pad * 8)) * glyph_pad * 8

            fragments = []
            for bitmap_row in bitmap:
                if len(bitmap_row) < bitmap_row_width:
                    bitmap_row = bitmap_row + [0] * (bitmap_row_width - len(bitmap_row))
                elif len(bitmap_row) > bitmap_row_width:
                    bitmap_row = bitmap_row[:bitmap_row_width]
                for i in range(bitmap_row_width // 8):
                    fragments.append(bitmap_row[i * 8:(i + 1) * 8])

            if self.table_format.ms_byte_first != self.table_format.ms_bit_first:
                _swap_fragments(fragments, scan_unit)

            bitmaps_size += buffer.write_binary_list(fragments, self.table_format.ms_bit_first)

        # Compat
        if self._compat_info is not None:
            bitmaps_sizes = list(self._compat_info)
            bitmaps_sizes[self.table_format.glyph_pad_index] = bitmaps_size
        else:
            bitmaps_sizes = [bitmaps_size // glyph_pad * glyph_pad_option for glyph_pad_option in PcfBitmaps.GLYPH_PAD_OPTIONS]

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format.value)
        buffer.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        buffer.write_uint32_list(bitmap_offsets, self.table_format.ms_byte_first)
        buffer.write_uint32_list(bitmaps_sizes, self.table_format.ms_byte_first)
        buffer.skip(bitmaps_size)
        buffer.align_to_bit32_with_nulls()

        table_size = buffer.tell() - table_offset
        return table_size
