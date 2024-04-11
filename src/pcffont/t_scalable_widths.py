from collections import UserList

from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfScalableWidths(PcfTable, UserList[int]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfScalableWidths':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)

        glyphs_count = buffer.read_int32(byte_order)
        scalable_widths = [buffer.read_int32(byte_order) for _ in range(glyphs_count)]

        return PcfScalableWidths(table_format, scalable_widths)

    def __init__(
            self,
            table_format: int = PcfTable.DEFAULT_TABLE_FORMAT,
            scalable_widths: list[int] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, scalable_widths)

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        byte_order = util.get_table_byte_order(self.table_format)

        glyphs_count = len(self)

        buffer.seek(table_offset)
        buffer.write_int32_le(self.table_format)
        buffer.write_int32(glyphs_count, byte_order)
        for scalable_width in self:
            buffer.write_int32(scalable_width, byte_order)

        table_size = buffer.tell() - table_offset
        return table_size
