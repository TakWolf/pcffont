from collections import UserList
from typing import Any

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfScalableWidths(PcfTable, UserList[int]):
    @staticmethod
    def parse(buffer: Buffer, _font: 'pcffont.PcfFont', header: PcfHeader, strict_level: int) -> 'PcfScalableWidths':
        table_format = header.read_and_check_table_format(buffer, strict_level)

        glyphs_count = buffer.read_uint32(table_format.ms_byte_first)

        scalable_widths = PcfScalableWidths(
            table_format,
            buffer.read_int32_list(glyphs_count, table_format.ms_byte_first),
        )
        return scalable_widths

    def __init__(
            self,
            table_format: PcfTableFormat = None,
            scalable_widths: list[int] = None,
    ):
        if table_format is None:
            table_format = PcfTableFormat()
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, scalable_widths)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfScalableWidths):
            return False
        return (self.table_format == other.table_format and
                UserList.__eq__(self, other))

    def _dump(self, buffer: Buffer, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyphs_count = len(self)

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format.value)
        buffer.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        buffer.write_int32_list(self, self.table_format.ms_byte_first)

        table_size = buffer.tell() - table_offset
        return table_size
