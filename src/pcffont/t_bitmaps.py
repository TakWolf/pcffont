from collections import UserList

from pcffont.error import PcfError
from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


def _get_bit_aligned_bitmap(bitmap: list[list[int]], n: int) -> list[list[int]]:
    new_bitmap = []
    for bitmap_row in bitmap:
        new_bitmap_row = []
        for i in range(n):
            if i < len(bitmap_row):
                new_bitmap_row.append(bitmap_row[i])
            else:
                new_bitmap_row.append(0)
        new_bitmap.append(new_bitmap_row)
    return new_bitmap


class PcfBitmaps(PcfTable, UserList[list[list[int]]]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfBitmaps':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)

        # How each row in each glyph's bitmap is padded
        # 0 => byte, 1 => short, 2 => int32, 3 => int64
        bitmap_padded_mode = table_format & 3
        bitmap_row_size = [1, 2, 4, 8][bitmap_padded_mode]

        # What the bits are stored
        # 0 => byte, 1 => short, 2 => int32
        bits_stored_mode = (table_format >> 4) & 3
        if bits_stored_mode != 0:
            raise PcfError(f'Table format not supported: {table_format:b}')

        glyphs_count = buffer.read_int32(byte_order)
        bitmap_offsets = [buffer.read_int32(byte_order) for _ in range(glyphs_count)]
        size_configs = [buffer.read_int32(byte_order) for _ in range(4)]
        bitmaps_start = buffer.tell()
        bitmaps_size = size_configs[bitmap_padded_mode]

        bitmaps = []
        for i in range(glyphs_count):
            bitmap_offset = bitmap_offsets[i]
            if i < glyphs_count - 1:
                bitmap_offset_next = bitmap_offsets[i + 1]
            else:
                bitmap_offset_next = bitmaps_size
            bitmap_size = bitmap_offset_next - bitmap_offset

            bitmap = []
            buffer.seek(bitmaps_start + bitmap_offset)
            for _ in range(bitmap_size // bitmap_row_size):
                bitmap_row = []
                for _ in range(bitmap_row_size):
                    data = buffer.read(1)
                    array = [int(c) for c in f'{ord(data):08b}']
                    if byte_order == 'little':
                        array.reverse()
                    bitmap_row.extend(array)
                bitmap.append(bitmap_row)
            bitmaps.append(bitmap)

        return PcfBitmaps(table_format, bitmaps, size_configs)

    def __init__(
            self,
            table_format: int = PcfTable.DEFAULT_TABLE_FORMAT,
            bitmaps: list[list[list[int]]] = None,
            _old_size_configs: list[int] = None,  # TODO
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, bitmaps)
        self._old_size_configs = _old_size_configs  # TODO

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        byte_order = util.get_table_byte_order(self.table_format)

        # How each row in each glyph's bitmap is padded
        # 0 => byte, 1 => short, 2 => int32, 3 => int64
        bitmap_padded_mode = self.table_format & 3
        bitmap_row_size = [1, 2, 4, 8][bitmap_padded_mode]

        # What the bits are stored
        # 0 => byte, 1 => short, 2 => int32
        bits_stored_mode = (self.table_format >> 4) & 3
        if bits_stored_mode != 0:
            raise PcfError(f'Table format not supported: {self.table_format:b}')

        glyphs_count = len(self)

        bitmaps_start = table_offset + 4 + 4 + 4 * glyphs_count + 4 * 4
        bitmaps_size = 0
        bitmap_offsets = []
        buffer.seek(bitmaps_start)
        for bitmap in self:
            bitmap_offsets.append(bitmaps_size)
            bitmap = _get_bit_aligned_bitmap(bitmap, 8 * bitmap_row_size)
            for bitmap_row in bitmap:
                for i in range(len(bitmap_row) // 8):
                    array = bitmap_row[i * 8:(i + 1) * 8]
                    if byte_order == 'little':
                        array.reverse()
                    bin_string = ''.join(map(str, array))
                    data = int(bin_string, 2).to_bytes(1, 'big')
                    bitmaps_size += buffer.write(data)

        # TODO
        if compat_mode and self._old_size_configs is not None:
            size_configs = list(self._old_size_configs)
            size_configs[bitmap_padded_mode] = bitmaps_size
        else:
            unit_size_config = bitmaps_size // bitmap_row_size
            size_configs = [
                unit_size_config,
                unit_size_config * 2,
                unit_size_config * 4,
                unit_size_config * 8,
            ]

        buffer.seek(table_offset)
        buffer.write_int32_le(self.table_format)
        buffer.write_int32(glyphs_count, byte_order)
        for offset in bitmap_offsets:
            buffer.write_int32(offset, byte_order)
        for size_config in size_configs:
            buffer.write_int32(size_config, byte_order)
        buffer.skip(bitmaps_size)

        table_size = buffer.tell() - table_offset
        return table_size
