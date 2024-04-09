from collections import UserList

from pcffont.header import PcfTableFormat, PcfHeader
from pcffont.internal.stream import Buffer
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
        table_format, byte_order = header.read_and_check_table_format(buffer)

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

        return PcfMetrics(metrics, is_compressed)

    def __init__(self, metrics: list[PcfMetric] = None, is_compressed: bool = True):
        super().__init__(metrics)
        self.is_compressed = is_compressed

    def _dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        table_format = 0b1110
        metrics_count = len(self)

        if self.is_compressed:
            table_format = table_format | PcfTableFormat.COMPRESSED_METRICS
            table_size = 4 + 2 + 5 * metrics_count
        else:
            table_size = 4 + 4 + 2 * 6 * metrics_count

        buffer.seek(table_offset)
        buffer.write_int32_le(table_format)
        if self.is_compressed:
            buffer.write_int16_be(metrics_count)
            for metric in self:
                buffer.write_int8_be(metric.left_sided_bearing)
                buffer.write_int8_be(metric.right_side_bearing)
                buffer.write_int8_be(metric.character_width)
                buffer.write_int8_be(metric.character_ascent)
                buffer.write_int8_be(metric.character_descent)
        else:
            buffer.write_int32_be(metrics_count)
            for metric in self:
                buffer.write_int16_be(metric.left_sided_bearing)
                buffer.write_int16_be(metric.right_side_bearing)
                buffer.write_int16_be(metric.character_width)
                buffer.write_int16_be(metric.character_ascent)
                buffer.write_int16_be(metric.character_descent)
                buffer.write_int16_be(metric.character_attributes)

        return table_format, table_size
