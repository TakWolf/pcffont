from collections import UserList
from typing import Any

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.stream import Stream


class PcfGlyphNames(UserList[str]):
    @staticmethod
    def parse(stream: Stream, _font: 'pcffont.PcfFont', header: PcfHeader) -> 'PcfGlyphNames':
        table_format = header.read_and_check_table_format(stream)

        glyphs_count = stream.read_uint32(table_format.ms_byte_first)
        name_offsets = stream.read_uint32_list(glyphs_count, table_format.ms_byte_first)
        stream.skip(4)  # strings_size
        strings_start = stream.tell()

        names = PcfGlyphNames(table_format)
        for name_offset in name_offsets:
            stream.seek(strings_start + name_offset)
            name = stream.read_string()
            names.append(name)
        return names

    table_format: PcfTableFormat

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            names: list[str] | None = None,
    ):
        super().__init__(names)
        self.table_format = PcfTableFormat() if table_format is None else table_format

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfGlyphNames):
            return False
        return (self.table_format == other.table_format and
                super().__eq__(other))

    def dump(self, stream: Stream, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyphs_count = len(self)

        strings_start = table_offset + 4 + 4 + 4 * glyphs_count + 4
        strings_size = 0
        name_offsets = []
        stream.seek(strings_start)
        for name in self:
            name_offsets.append(strings_size)
            strings_size += stream.write_string(name)

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        stream.write_uint32_list(name_offsets, self.table_format.ms_byte_first)
        stream.write_uint32(strings_size, self.table_format.ms_byte_first)
        stream.skip(strings_size)
        stream.align_to_bit32_with_nulls()

        table_size = stream.tell() - table_offset
        return table_size
