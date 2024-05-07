from collections import UserList
from copy import copy
from typing import Any

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

        if table_format.ink_or_compressed_metrics:
            glyphs_count = buffer.read_uint16(table_format.ms_byte_first)
        else:
            glyphs_count = buffer.read_uint32(table_format.ms_byte_first)

        metrics = PcfMetrics(table_format)
        for _ in range(glyphs_count):
            metric = PcfMetric.parse(buffer, table_format.ms_byte_first, table_format.ink_or_compressed_metrics)
            metrics.append(metric)
        return metrics

    def __init__(
            self,
            table_format: PcfTableFormat = None,
            metrics: list[PcfMetric] = None,
    ):
        if table_format is None:
            table_format = PcfTableFormat()
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, metrics)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfMetrics):
            return False
        return (self.table_format == other.table_format and
                UserList.__eq__(self, other))

    def calculate_min_bounds(self) -> PcfMetric:
        min_bounds = None
        for metric in self:
            if min_bounds is None:
                min_bounds = copy(metric)
            else:
                min_bounds.left_side_bearing = min(min_bounds.left_side_bearing, metric.left_side_bearing)
                min_bounds.right_side_bearing = min(min_bounds.right_side_bearing, metric.right_side_bearing)
                min_bounds.character_width = min(min_bounds.character_width, metric.character_width)
                min_bounds.ascent = min(min_bounds.ascent, metric.ascent)
                min_bounds.descent = min(min_bounds.descent, metric.descent)
        return min_bounds

    def calculate_max_bounds(self) -> PcfMetric:
        max_bounds = None
        for metric in self:
            if max_bounds is None:
                max_bounds = copy(metric)
            else:
                max_bounds.left_side_bearing = max(max_bounds.left_side_bearing, metric.left_side_bearing)
                max_bounds.right_side_bearing = max(max_bounds.right_side_bearing, metric.right_side_bearing)
                max_bounds.character_width = max(max_bounds.character_width, metric.character_width)
                max_bounds.ascent = max(max_bounds.ascent, metric.ascent)
                max_bounds.descent = max(max_bounds.descent, metric.descent)
        return max_bounds

    def calculate_max_overlap(self) -> int:
        return max([metric.right_side_bearing - metric.character_width for metric in self])

    def calculate_compressible(self) -> bool:
        return all([metric.compressible for metric in self])

    def _dump(self, buffer: Buffer, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyphs_count = len(self)

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format.value)
        if self.table_format.ink_or_compressed_metrics:
            buffer.write_uint16(glyphs_count, self.table_format.ms_byte_first)
        else:
            buffer.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        for metric in self:
            metric.dump(buffer, self.table_format.ms_byte_first, self.table_format.ink_or_compressed_metrics)

        table_size = buffer.tell() - table_offset
        return table_size
