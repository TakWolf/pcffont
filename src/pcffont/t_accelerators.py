from typing import Any

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.stream import Stream
from pcffont.metric import PcfMetric


class PcfAccelerators:
    @staticmethod
    def parse(stream: Stream, _font: 'pcffont.PcfFont', header: PcfHeader) -> 'PcfAccelerators':
        table_format = header.read_and_check_table_format(stream)

        no_overlap = stream.read_bool()
        constant_metrics = stream.read_bool()
        terminal_font = stream.read_bool()
        constant_width = stream.read_bool()
        ink_inside = stream.read_bool()
        ink_metrics = stream.read_bool()
        draw_right_to_left = stream.read_bool()
        stream.skip(1)
        font_ascent = stream.read_int32(table_format.ms_byte_first)
        font_descent = stream.read_int32(table_format.ms_byte_first)
        max_overlap = stream.read_int32(table_format.ms_byte_first)

        min_bounds = PcfMetric.parse(stream, table_format.ms_byte_first, False)
        max_bounds = PcfMetric.parse(stream, table_format.ms_byte_first, False)

        if table_format.ink_or_compressed_metrics:
            ink_min_bounds = PcfMetric.parse(stream, table_format.ms_byte_first, False)
            ink_max_bounds = PcfMetric.parse(stream, table_format.ms_byte_first, False)
        else:
            ink_min_bounds = None
            ink_max_bounds = None

        # Compat
        if header.table_size > stream.tell() - header.table_offset:
            stream.seek(header.table_offset)
            raw_chunk = stream.read(header.table_size, ignore_eof=True)
            _compat_info = raw_chunk, header.table_size
        else:
            _compat_info = None

        accelerators = PcfAccelerators(
            table_format,
            no_overlap,
            constant_metrics,
            terminal_font,
            constant_width,
            ink_inside,
            ink_metrics,
            draw_right_to_left,
            font_ascent,
            font_descent,
            max_overlap,
            min_bounds,
            max_bounds,
            ink_min_bounds,
            ink_max_bounds,
        )

        # Compat
        accelerators._compat_info = _compat_info

        return accelerators

    table_format: PcfTableFormat
    no_overlap: bool
    constant_metrics: bool
    terminal_font: bool
    constant_width: bool
    ink_inside: bool
    ink_metrics: bool
    draw_right_to_left: bool
    font_ascent: int
    font_descent: int
    max_overlap: int
    min_bounds: PcfMetric | None
    max_bounds: PcfMetric | None
    ink_min_bounds: PcfMetric | None
    ink_max_bounds: PcfMetric | None
    _compat_info: tuple[bytes, int] | None

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            no_overlap: bool = False,
            constant_metrics: bool = False,
            terminal_font: bool = False,
            constant_width: bool = False,
            ink_inside: bool = False,
            ink_metrics: bool = False,
            draw_right_to_left: bool = False,
            font_ascent: int = 0,
            font_descent: int = 0,
            max_overlap: int = 0,
            min_bounds: PcfMetric | None = None,
            max_bounds: PcfMetric | None = None,
            ink_min_bounds: PcfMetric | None = None,
            ink_max_bounds: PcfMetric | None = None,
    ):
        self.table_format = PcfTableFormat() if table_format is None else table_format
        self.no_overlap = no_overlap
        self.constant_metrics = constant_metrics
        self.terminal_font = terminal_font
        self.constant_width = constant_width
        self.ink_inside = ink_inside
        self.ink_metrics = ink_metrics
        self.draw_right_to_left = draw_right_to_left
        self.font_ascent = font_ascent
        self.font_descent = font_descent
        self.max_overlap = max_overlap
        self.min_bounds = min_bounds
        self.max_bounds = max_bounds
        self.ink_min_bounds = ink_min_bounds
        self.ink_max_bounds = ink_max_bounds
        self._compat_info = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfAccelerators):
            return False
        return (self.table_format == other.table_format and
                self.no_overlap == other.no_overlap and
                self.constant_metrics == other.constant_metrics and
                self.terminal_font == other.terminal_font and
                self.constant_width == other.constant_width and
                self.ink_inside == other.ink_inside and
                self.ink_metrics == other.ink_metrics and
                self.draw_right_to_left == other.draw_right_to_left and
                self.font_ascent == other.font_ascent and
                self.font_descent == other.font_descent and
                self.max_overlap == other.max_overlap and
                self.min_bounds == other.min_bounds and
                self.max_bounds == other.max_bounds and
                self.ink_min_bounds == other.ink_min_bounds and
                self.ink_max_bounds == other.ink_max_bounds and
                self._compat_info == other._compat_info)

    def dump(self, stream: Stream, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_bool(self.no_overlap)
        stream.write_bool(self.constant_metrics)
        stream.write_bool(self.terminal_font)
        stream.write_bool(self.constant_width)
        stream.write_bool(self.ink_inside)
        stream.write_bool(self.ink_metrics)
        stream.write_bool(self.draw_right_to_left)
        stream.write_nulls(1)
        stream.write_int32(self.font_ascent, self.table_format.ms_byte_first)
        stream.write_int32(self.font_descent, self.table_format.ms_byte_first)
        stream.write_int32(self.max_overlap, self.table_format.ms_byte_first)

        self.min_bounds.dump(stream, self.table_format.ms_byte_first, False)
        self.max_bounds.dump(stream, self.table_format.ms_byte_first, False)

        if self.table_format.ink_or_compressed_metrics:
            self.ink_min_bounds.dump(stream, self.table_format.ms_byte_first, False)
            self.ink_max_bounds.dump(stream, self.table_format.ms_byte_first, False)

        # Compat
        if self._compat_info is not None:
            raw_chunk, table_size = self._compat_info
            stream.write(raw_chunk[stream.tell() - table_offset::])
        else:
            stream.align_to_bit32_with_nulls()
            table_size = stream.tell() - table_offset

        return table_size
