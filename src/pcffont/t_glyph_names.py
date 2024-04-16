from collections import UserList

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfGlyphNames(PcfTable, UserList[str]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfGlyphNames':
        table_format = PcfTableFormat.read_and_check(buffer, header)
        is_ms_byte = PcfTableFormat.is_ms_byte(table_format)

        glyphs_count = buffer.read_int32(is_ms_byte)
        name_offsets = [buffer.read_int32(is_ms_byte) for _ in range(glyphs_count)]
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
        is_ms_byte = PcfTableFormat.is_ms_byte(self.table_format)

        glyphs_count = len(self)

        strings_start = table_offset + 4 + 4 + 4 * glyphs_count + 4
        strings_size = 0
        name_offsets = []
        buffer.seek(strings_start)
        for name in self:
            name_offsets.append(strings_size)
            strings_size += buffer.write_string(name)

        buffer.seek(table_offset)
        buffer.write_int32(self.table_format)
        buffer.write_int32(glyphs_count, is_ms_byte)
        for name_offset in name_offsets:
            buffer.write_int32(name_offset, is_ms_byte)
        buffer.write_int32(strings_size, is_ms_byte)
        buffer.skip(strings_size)

        table_size = buffer.tell() - table_offset
        return table_size
