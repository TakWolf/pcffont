from collections import UserList

from pcffont.header import PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.table import PcfTable


class PcfGlyphNames(PcfTable, UserList[str]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfGlyphNames':
        _, byte_order = header.get_and_check_table_format(buffer)

        glyphs_count = buffer.read_int32(byte_order)
        name_offsets = [buffer.read_int32(byte_order) for _ in range(glyphs_count)]
        buffer.skip_int()  # strings_size
        strings_start = buffer.tell()

        names = []
        for name_offset in name_offsets:
            buffer.seek(strings_start + name_offset)
            name = buffer.read_string()
            names.append(name)

        return PcfGlyphNames(names)

    def __init__(self, names: list[str] = None):
        super().__init__(names)

    def _dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        table_format = 0b1110
        glyphs_count = len(self)

        strings_start = table_offset + 4 + 4 + 4 * glyphs_count + 4
        strings_size = 0
        name_offsets = []
        buffer.seek(strings_start)
        for name in self:
            name_offsets.append(strings_size)
            strings_size += buffer.write_string(name)

        table_size = strings_start - table_offset + strings_size

        buffer.seek(table_offset)
        buffer.write_int32_le(table_format)
        buffer.write_int32_be(glyphs_count)
        for name_offset in name_offsets:
            buffer.write_int32_be(name_offset)
        buffer.write_int32_be(strings_size)

        return table_format, table_size
