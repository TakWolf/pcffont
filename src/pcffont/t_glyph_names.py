from collections import UserList
from typing import Any

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfGlyphNames(PcfTable, UserList[str]):
    @staticmethod
    def parse(buffer: Buffer, _font: 'pcffont.PcfFont', header: PcfHeader, strict_level: int) -> 'PcfGlyphNames':
        table_format = header.read_and_check_table_format(buffer, strict_level)

        glyphs_count = buffer.read_uint32(table_format.ms_byte_first)
        name_offsets = buffer.read_uint32_list(glyphs_count, table_format.ms_byte_first)
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
            table_format: PcfTableFormat = None,
            names: list[str] = None,
    ):
        if table_format is None:
            table_format = PcfTableFormat()
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, names)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfGlyphNames):
            return False
        return (self.table_format == other.table_format and
                UserList.__eq__(self, other))

    def _dump(self, buffer: Buffer, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyphs_count = len(self)

        strings_start = table_offset + 4 + 4 + 4 * glyphs_count + 4
        strings_size = 0
        name_offsets = []
        buffer.seek(strings_start)
        for name in self:
            name_offsets.append(strings_size)
            strings_size += buffer.write_string(name)

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format.value)
        buffer.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        buffer.write_uint32_list(name_offsets, self.table_format.ms_byte_first)
        buffer.write_uint32(strings_size, self.table_format.ms_byte_first)
        buffer.skip(strings_size)

        table_size = buffer.tell() - table_offset
        return table_size
