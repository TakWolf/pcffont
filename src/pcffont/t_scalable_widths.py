from collections import UserList

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfScalableWidths(PcfTable, UserList[int]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfScalableWidths':
        table_format = PcfTableFormat.read_and_check(buffer, header)
        ms_byte_first = PcfTableFormat.ms_byte_first(table_format)

        glyphs_count = buffer.read_uint32(ms_byte_first)

        scalable_widths = PcfScalableWidths(
            table_format,
            buffer.read_int32_list(glyphs_count, ms_byte_first),
        )
        return scalable_widths

    def __init__(
            self,
            table_format: int = PcfTableFormat.build(),
            scalable_widths: list[int] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, scalable_widths)

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        ms_byte_first = PcfTableFormat.ms_byte_first(self.table_format)

        glyphs_count = len(self)

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format)
        buffer.write_uint32(glyphs_count, ms_byte_first)
        buffer.write_int32_list(self, ms_byte_first)

        table_size = buffer.tell() - table_offset
        return table_size
