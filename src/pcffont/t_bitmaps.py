from collections import UserList

from pcffont.error import PcfError
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfBitmaps(PcfTable, UserList[list[list[int]]]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfBitmaps':
        table_format = PcfTableFormat.read_and_check(buffer, header)
        ms_byte_first = PcfTableFormat.ms_byte_first(table_format)
        ms_bit_first = PcfTableFormat.ms_bit_first(table_format)

        glyph_pad_config = PcfTableFormat.glyph_pad_config(table_format)
        glyph_pad = [1, 2, 4, 8][glyph_pad_config]

        # FIXME
        scan_unit_config = PcfTableFormat.scan_unit_config(table_format)
        scan_unit = [1, 2, 4][scan_unit_config]
        if scan_unit != 1:
            raise PcfError(f'Table format not supported: {table_format:b}')

        glyphs_count = buffer.read_uint32(ms_byte_first)
        bitmap_offsets = buffer.read_uint32_list(glyphs_count, ms_byte_first)
        bitmaps_sizes = buffer.read_uint32_list(4, ms_byte_first)
        bitmaps_start = buffer.tell()
        bitmaps_size = bitmaps_sizes[glyph_pad_config]

        bitmaps = PcfBitmaps(table_format)
        for i in range(glyphs_count):
            bitmap_offset = bitmap_offsets[i]
            if i < glyphs_count - 1:
                bitmap_offset_next = bitmap_offsets[i + 1]
            else:
                bitmap_offset_next = bitmaps_size
            bitmap_size = bitmap_offset_next - bitmap_offset

            bitmap = []
            buffer.seek(bitmaps_start + bitmap_offset)
            for _ in range(bitmap_size // glyph_pad):
                bin_format = '{:0' + str(glyph_pad * 8) + 'b}'
                bin_string = bin_format.format(buffer.read_uint(glyph_pad, ms_byte_first))
                bitmap_row = [int(c) for c in bin_string]
                if not ms_bit_first:
                    bitmap_row.reverse()
                bitmap.append(bitmap_row)
            bitmaps.append(bitmap)

        # Compat
        bitmaps._compat_info = bitmaps_sizes

        return bitmaps

    def __init__(
            self,
            table_format: int = PcfTableFormat.build(),
            bitmaps: list[list[list[int]]] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, bitmaps)
        self._compat_info: list[int] | None = None

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        ms_byte_first = PcfTableFormat.ms_byte_first(self.table_format)
        ms_bit_first = PcfTableFormat.ms_byte_first(self.table_format)

        glyph_pad_config = PcfTableFormat.glyph_pad_config(self.table_format)
        glyph_pad = [1, 2, 4, 8][glyph_pad_config]

        # FIXME
        scan_unit_config = PcfTableFormat.scan_unit_config(self.table_format)
        scan_unit = [1, 2, 4][scan_unit_config]
        if scan_unit != 1:
            raise PcfError(f'Table format not supported: {self.table_format:b}')

        glyphs_count = len(self)

        bitmaps_start = table_offset + 4 + 4 + 4 * glyphs_count + 4 * 4
        bitmaps_size = 0
        bitmap_offsets = []
        buffer.seek(bitmaps_start)
        for bitmap in self:
            bitmap_offsets.append(bitmaps_size)
            for bitmap_row in bitmap:
                if len(bitmap_row) < 8 * glyph_pad:
                    bitmap_row = bitmap_row + [0] * (8 * glyph_pad - len(bitmap_row))
                if not ms_bit_first:
                    bitmap_row = bitmap_row[::-1]
                bin_string = ''.join(map(str, bitmap_row))
                bitmaps_size += buffer.write_uint(int(bin_string, 2), glyph_pad, ms_byte_first)

        # Compat
        if self._compat_info is not None:
            bitmaps_sizes = list(self._compat_info)
            bitmaps_sizes[glyph_pad_config] = bitmaps_size
        else:
            unit_bitmaps_size = bitmaps_size // glyph_pad
            bitmaps_sizes = [
                unit_bitmaps_size,
                unit_bitmaps_size * 2,
                unit_bitmaps_size * 4,
                unit_bitmaps_size * 8,
            ]

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format)
        buffer.write_uint32(glyphs_count, ms_byte_first)
        buffer.write_uint32_list(bitmap_offsets, ms_byte_first)
        buffer.write_uint32_list(bitmaps_sizes, ms_byte_first)
        buffer.skip(bitmaps_size)

        table_size = buffer.tell() - table_offset
        return table_size
