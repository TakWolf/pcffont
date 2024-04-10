from collections import UserList

from pcffont.header import PcfTableFormat, PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfMetric:
    def __init__(
            self,
            left_sided_bearing: int,
            right_side_bearing: int,
            character_width: int,
            character_ascent: int,
            character_descent: int,
            character_attributes: int = 0,
    ):
        self.left_sided_bearing = left_sided_bearing
        self.right_side_bearing = right_side_bearing
        self.character_width = character_width
        self.character_ascent = character_ascent
        self.character_descent = character_descent
        self.character_attributes = character_attributes


class PcfMetrics(PcfTable, UserList[PcfMetric]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfMetrics':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)

        metrics = []
        is_compressed = table_format & PcfTableFormat.COMPRESSED_METRICS > 0
        if is_compressed:
            metrics_count = buffer.read_int16(byte_order)
            for _ in range(metrics_count):
                left_sided_bearing = buffer.read_int8(byte_order)
                right_side_bearing = buffer.read_int8(byte_order)
                character_width = buffer.read_int8(byte_order)
                character_ascent = buffer.read_int8(byte_order)
                character_descent = buffer.read_int8(byte_order)
                metrics.append(PcfMetric(
                    left_sided_bearing,
                    right_side_bearing,
                    character_width,
                    character_ascent,
                    character_descent,
                ))
        else:
            metrics_count = buffer.read_int32(byte_order)
            for _ in range(metrics_count):
                left_sided_bearing = buffer.read_int16(byte_order)
                right_side_bearing = buffer.read_int16(byte_order)
                character_width = buffer.read_int16(byte_order)
                character_ascent = buffer.read_int16(byte_order)
                character_descent = buffer.read_int16(byte_order)
                character_attributes = buffer.read_int16(byte_order)
                metrics.append(PcfMetric(
                    left_sided_bearing,
                    right_side_bearing,
                    character_width,
                    character_ascent,
                    character_descent,
                    character_attributes,
                ))

        return PcfMetrics(table_format, metrics)

    def __init__(
            self,
            table_format: int = 0b1110 | PcfTableFormat.COMPRESSED_METRICS,
            metrics: list[PcfMetric] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, metrics)

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        byte_order = util.get_table_byte_order(self.table_format)
        is_compressed = self.table_format & PcfTableFormat.COMPRESSED_METRICS > 0

        metrics_count = len(self)

        if is_compressed:
            table_size = 4 + 2 + 5 * metrics_count
        else:
            table_size = 4 + 4 + 2 * 6 * metrics_count

        buffer.seek(table_offset)
        buffer.write_int32_le(self.table_format)
        if is_compressed:
            buffer.write_int16(metrics_count, byte_order)
            for metric in self:
                buffer.write_int8(metric.left_sided_bearing, byte_order)
                buffer.write_int8(metric.right_side_bearing, byte_order)
                buffer.write_int8(metric.character_width, byte_order)
                buffer.write_int8(metric.character_ascent, byte_order)
                buffer.write_int8(metric.character_descent, byte_order)
        else:
            buffer.write_int32(metrics_count, byte_order)
            for metric in self:
                buffer.write_int16(metric.left_sided_bearing, byte_order)
                buffer.write_int16(metric.right_side_bearing, byte_order)
                buffer.write_int16(metric.character_width, byte_order)
                buffer.write_int16(metric.character_ascent, byte_order)
                buffer.write_int16(metric.character_descent, byte_order)
                buffer.write_int16(metric.character_attributes, byte_order)

        return table_size
