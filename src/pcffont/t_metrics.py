from collections import UserList

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.metric import PcfMetric
from pcffont.table import PcfTable


class PcfMetrics(PcfTable, UserList[PcfMetric]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfMetrics':
        table_format = PcfTableFormat.read_and_check(buffer, header)
        is_ms_byte = PcfTableFormat.is_ms_byte(table_format)
        is_compressed = PcfTableFormat.is_compressed_metrics(table_format)

        if is_compressed:
            glyphs_count = buffer.read_int16(is_ms_byte)
        else:
            glyphs_count = buffer.read_int32(is_ms_byte)
        metrics = [PcfMetric.parse(buffer, is_ms_byte, is_compressed) for _ in range(glyphs_count)]

        return PcfMetrics(table_format, metrics)

    def __init__(
            self,
            table_format: int = PcfTableFormat.build_for_metrics(),
            metrics: list[PcfMetric] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, metrics)

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        is_ms_byte = PcfTableFormat.is_ms_byte(self.table_format)
        is_compressed = PcfTableFormat.is_compressed_metrics(self.table_format)

        glyphs_count = len(self)

        buffer.seek(table_offset)
        buffer.write_int32(self.table_format)
        if is_compressed:
            buffer.write_int16(glyphs_count, is_ms_byte)
        else:
            buffer.write_int32(glyphs_count, is_ms_byte)
        for metric in self:
            metric.dump(buffer, is_ms_byte, is_compressed)

        table_size = buffer.tell() - table_offset
        return table_size
