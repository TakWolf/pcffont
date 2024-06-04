from collections import UserList
from typing import Any

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer


class PcfScalableWidths(UserList[int]):
    @staticmethod
    def parse(buffer: Buffer, _font: 'pcffont.PcfFont', header: PcfHeader, strict_level: int) -> 'PcfScalableWidths':
        table_format = header.read_and_check_table_format(buffer, strict_level)

        glyphs_count = buffer.read_uint32(table_format.ms_byte_first)

        scalable_widths = PcfScalableWidths(
            table_format,
            buffer.read_int32_list(glyphs_count, table_format.ms_byte_first),
        )
        return scalable_widths

    table_format: PcfTableFormat

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            scalable_widths: list[int] | None = None,
    ):
        super().__init__(scalable_widths)
        if table_format is None:
            table_format = PcfTableFormat()
        self.table_format = table_format

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfScalableWidths):
            return False
        return (self.table_format == other.table_format and
                super().__eq__(other))

    def dump(self, buffer: Buffer, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyphs_count = len(self)

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format.value)
        buffer.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        buffer.write_int32_list(self, self.table_format.ms_byte_first)
        buffer.align_to_bit32_with_nulls()

        table_size = buffer.tell() - table_offset
        return table_size
