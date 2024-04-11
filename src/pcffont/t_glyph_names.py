from collections import UserList

from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfGlyphNames(PcfTable, UserList[str]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfGlyphNames':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)

        glyphs_count = buffer.read_int32(byte_order)
        name_offsets = [buffer.read_int32(byte_order) for _ in range(glyphs_count)]
        buffer.skip_int()  # strings_size
        strings_start = buffer.tell()

        names = []
        for name_offset in name_offsets:
            buffer.seek(strings_start + name_offset)
            name = buffer.read_string()
            names.append(name)

        return PcfGlyphNames(table_format, names)

    def __init__(
            self,
            table_format: int = PcfTable.DEFAULT_TABLE_FORMAT,
            names: list[str] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, names)

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        byte_order = util.get_table_byte_order(self.table_format)

        glyphs_count = len(self)

        strings_start = table_offset + 4 + 4 + 4 * glyphs_count + 4
        strings_size = 0
        name_offsets = []
        buffer.seek(strings_start)
        for name in self:
            name_offsets.append(strings_size)
            strings_size += buffer.write_string(name)

        buffer.seek(table_offset)
        buffer.write_int32_le(self.table_format)
        buffer.write_int32(glyphs_count, byte_order)
        for name_offset in name_offsets:
            buffer.write_int32(name_offset, byte_order)
        buffer.write_int32(strings_size, byte_order)
        buffer.skip(strings_size)

        table_size = buffer.tell() - table_offset
        return table_size
