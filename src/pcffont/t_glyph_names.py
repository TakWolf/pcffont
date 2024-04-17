from collections import UserList

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfGlyphNames(PcfTable, UserList[str]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfGlyphNames':
        table_format = PcfTableFormat.read_and_check(buffer, header)
        ms_byte_first = PcfTableFormat.ms_byte_first(table_format)

        glyphs_count = buffer.read_uint32(ms_byte_first)
        name_offsets = [buffer.read_uint32(ms_byte_first) for _ in range(glyphs_count)]
        buffer.skip(4)  # strings_size
        strings_start = buffer.tell()

        names = PcfGlyphNames(table_format)
        for name_offset in name_offsets:
            buffer.seek(strings_start + name_offset)
            name = buffer.read_string()
            names.append(name)
        return names

    def __init__(
            self,
            table_format: int = PcfTableFormat.build(),
            names: list[str] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, names)

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        ms_byte_first = PcfTableFormat.ms_byte_first(self.table_format)

        glyphs_count = len(self)

        strings_start = table_offset + 4 + 4 + 4 * glyphs_count + 4
        strings_size = 0
        name_offsets = []
        buffer.seek(strings_start)
        for name in self:
            name_offsets.append(strings_size)
            strings_size += buffer.write_string(name)

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format)
        buffer.write_uint32(glyphs_count, ms_byte_first)
        for name_offset in name_offsets:
            buffer.write_uint32(name_offset, ms_byte_first)
        buffer.write_uint32(strings_size, ms_byte_first)
        buffer.skip(strings_size)

        table_size = buffer.tell() - table_offset
        return table_size
