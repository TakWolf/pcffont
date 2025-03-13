from collections import UserList
from copy import copy
from typing import Any

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.stream import Stream
from pcffont.metric import PcfMetric


class PcfMetrics(UserList[PcfMetric]):
    @staticmethod
    def parse(stream: Stream, _font: 'pcffont.PcfFont', header: PcfHeader) -> 'PcfMetrics':
        table_format = header.read_and_check_table_format(stream)

        if table_format.ink_or_compressed_metrics:
            glyphs_count = stream.read_uint16(table_format.ms_byte_first)
        else:
            glyphs_count = stream.read_uint32(table_format.ms_byte_first)

        metrics = PcfMetrics(table_format)
        for _ in range(glyphs_count):
            metric = PcfMetric.parse(stream, table_format.ms_byte_first, table_format.ink_or_compressed_metrics)
            metrics.append(metric)
        return metrics

    table_format: PcfTableFormat

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            metrics: list[PcfMetric] | None = None,
    ):
        super().__init__(metrics)
        self.table_format = PcfTableFormat() if table_format is None else table_format

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfMetrics):
            return False
        return (self.table_format == other.table_format and
                super().__eq__(other))

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
        return max(metric.right_side_bearing - metric.character_width for metric in self)

    def calculate_compressible(self) -> bool:
        return all(metric.compressible for metric in self)

    def dump(self, stream: Stream, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        glyphs_count = len(self)

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        if self.table_format.ink_or_compressed_metrics:
            stream.write_uint16(glyphs_count, self.table_format.ms_byte_first)
        else:
            stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        for metric in self:
            metric.dump(stream, self.table_format.ms_byte_first, self.table_format.ink_or_compressed_metrics)
        stream.align_to_bit32_with_nulls()

        table_size = stream.tell() - table_offset
        return table_size
