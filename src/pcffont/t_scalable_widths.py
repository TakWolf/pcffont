from collections import UserList

from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.table import PcfTable


class PcfScalableWidths(PcfTable, UserList[int]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfScalableWidths':
        _, byte_order = header.get_and_check_table_format(buffer)

        glyphs_count = buffer.read_int(byte_order)
        scalable_widths = [buffer.read_int(byte_order) for _ in range(glyphs_count)]

        return PcfScalableWidths(scalable_widths)

    def __init__(self, scalable_widths: list[int] = None):
        super().__init__(scalable_widths)

    @property
    def table_type(self) -> PcfTableType:
        return PcfTableType.SWIDTHS

    def dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        table_format = 0b1110
        glyphs_count = len(self)
        table_size = 4 + 4 + 4 * glyphs_count

        buffer.seek(table_offset)
        buffer.write_int_le(table_format)
        buffer.write_int_be(glyphs_count)
        for scalable_width in self:
            buffer.write_int_be(scalable_width)

        return table_format, table_size
