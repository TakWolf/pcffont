from collections import UserList

from pcffont.header import PcfTableFormat, PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.metric import PcfMetric
from pcffont.table import PcfTable


class PcfMetrics(PcfTable, UserList[PcfMetric]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfMetrics':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)
        is_compressed = table_format & PcfTableFormat.COMPRESSED_METRICS > 0

        if is_compressed:
            metrics_count = buffer.read_int16(byte_order)
        else:
            metrics_count = buffer.read_int32(byte_order)
        metrics = [PcfMetric.parse(buffer, byte_order, is_compressed) for _ in range(metrics_count)]

        return PcfMetrics(table_format, metrics)

    def __init__(
            self,
            table_format: int = PcfTable.DEFAULT_TABLE_FORMAT | PcfTableFormat.COMPRESSED_METRICS,
            metrics: list[PcfMetric] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, metrics)

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        byte_order = util.get_table_byte_order(self.table_format)
        is_compressed = self.table_format & PcfTableFormat.COMPRESSED_METRICS > 0

        metrics_count = len(self)

        buffer.seek(table_offset)
        buffer.write_int32_le(self.table_format)
        if is_compressed:
            buffer.write_int16(metrics_count, byte_order)
        else:
            buffer.write_int32(metrics_count, byte_order)
        for metric in self:
            metric.dump(buffer, byte_order, is_compressed)

        table_size = buffer.tell() - table_offset
        return table_size
