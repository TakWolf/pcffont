from collections import UserList

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.metric import PcfMetric
from pcffont.table import PcfTable


class PcfMetrics(PcfTable, UserList[PcfMetric]):
    @staticmethod
    def parse(buffer: Buffer, _font: 'pcffont.PcfFont', header: PcfHeader, strict_level: int) -> 'PcfMetrics':
        table_format = header.read_and_check_table_format(buffer, strict_level)

        if table_format.is_compressed_metrics:
            glyphs_count = buffer.read_uint16(table_format.ms_byte_first)
        else:
            glyphs_count = buffer.read_uint32(table_format.ms_byte_first)

        metrics = PcfMetrics(table_format)
        for _ in range(glyphs_count):
            metric = PcfMetric.parse(buffer, table_format.ms_byte_first, table_format.is_compressed_metrics)
            metrics.append(metric)
        return metrics

    def __init__(
            self,
            table_format: PcfTableFormat = None,
            metrics: list[PcfMetric] = None,
    ):
        if table_format is None:
            table_format = PcfTableFormat(is_compressed_metrics=True)
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, metrics)

    def _dump(self, buffer: Buffer, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyphs_count = len(self)

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format.value)
        if self.table_format.is_compressed_metrics:
            buffer.write_uint16(glyphs_count, self.table_format.ms_byte_first)
        else:
            buffer.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        for metric in self:
            metric.dump(buffer, self.table_format.ms_byte_first, self.table_format.is_compressed_metrics)

        table_size = buffer.tell() - table_offset
        return table_size
