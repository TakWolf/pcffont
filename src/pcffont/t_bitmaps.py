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
        is_ms_byte = PcfTableFormat.is_ms_byte(table_format)
        is_ms_bit = PcfTableFormat.is_ms_bit(table_format)

        bitmap_pad_mode = PcfTableFormat.bitmap_pad_mode(table_format)
        bitmap_row_size = [1, 2, 4, 8][bitmap_pad_mode]

        # FIXME
        bit_scan_mode = PcfTableFormat.bit_scan_mode(table_format)
        if bit_scan_mode != 0:
            raise PcfError(f'Table format not supported: {table_format:b}')

        glyphs_count = buffer.read_int32(is_ms_byte)
        bitmap_offsets = [buffer.read_int32(is_ms_byte) for _ in range(glyphs_count)]
        size_configs = [buffer.read_int32(is_ms_byte) for _ in range(4)]
        bitmaps_start = buffer.tell()
        bitmaps_size = size_configs[bitmap_pad_mode]

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
            for _ in range(bitmap_size // bitmap_row_size):
                bitmap_row = []
                for _ in range(bitmap_row_size):
                    data = buffer.read(1)
                    array = [int(c) for c in f'{ord(data):08b}']
                    if not is_ms_bit:
                        array.reverse()
                    bitmap_row.extend(array)
                bitmap.append(bitmap_row)
            bitmaps.append(bitmap)

        # TODO
        bitmaps._compat_size_configs = size_configs

        return bitmaps

    def __init__(
            self,
            table_format: int = PcfTableFormat.build(),
            bitmaps: list[list[list[int]]] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, bitmaps)
        self._compat_size_configs: list[int] | None = None  # TODO

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        is_ms_byte = PcfTableFormat.is_ms_byte(self.table_format)
        is_ms_bit = PcfTableFormat.is_ms_byte(self.table_format)

        bitmap_pad_mode = PcfTableFormat.bitmap_pad_mode(self.table_format)
        bitmap_row_size = [1, 2, 4, 8][bitmap_pad_mode]

        # FIXME
        bit_scan_mode = PcfTableFormat.bit_scan_mode(self.table_format)
        if bit_scan_mode != 0:
            raise PcfError(f'Table format not supported: {self.table_format:b}')

        glyphs_count = len(self)

        bitmaps_start = table_offset + 4 + 4 + 4 * glyphs_count + 4 * 4
        bitmaps_size = 0
        bitmap_offsets = []
        buffer.seek(bitmaps_start)
        for bitmap in self:
            bitmap_offsets.append(bitmaps_size)
            for bitmap_row in bitmap:
                if len(bitmap_row) < 8 * bitmap_row_size:
                    bitmap_row = bitmap_row[:]
                    bitmap_row += [0] * (8 * bitmap_row_size - len(bitmap_row))
                for i in range(len(bitmap_row) // 8):
                    array = bitmap_row[i * 8:(i + 1) * 8]
                    if not is_ms_bit:
                        array.reverse()
                    bin_string = ''.join(map(str, array))
                    data = int(bin_string, 2).to_bytes(1, 'big')
                    bitmaps_size += buffer.write(data)

        # TODO
        if compat_mode and self._compat_size_configs is not None:
            size_configs = list(self._compat_size_configs)
            size_configs[bitmap_pad_mode] = bitmaps_size
        else:
            unit_size_config = bitmaps_size // bitmap_row_size
            size_configs = [
                unit_size_config,
                unit_size_config * 2,
                unit_size_config * 4,
                unit_size_config * 8,
            ]

        buffer.seek(table_offset)
        buffer.write_int32(self.table_format)
        buffer.write_int32(glyphs_count, is_ms_byte)
        for offset in bitmap_offsets:
            buffer.write_int32(offset, is_ms_byte)
        for size_config in size_configs:
            buffer.write_int32(size_config, is_ms_byte)
        buffer.skip(bitmaps_size)

        table_size = buffer.tell() - table_offset
        return table_size
