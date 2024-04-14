from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.metric import PcfMetric
from pcffont.table import PcfTable


class PcfAccelerators(PcfTable):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfAccelerators':
        table_format = PcfTableFormat.read_and_check(buffer, header)
        is_ms_byte = PcfTableFormat.is_ms_byte(table_format)
        has_ink_bounds = PcfTableFormat.has_ink_bounds(table_format)

        no_overlap = buffer.read_bool()
        constant_metrics = buffer.read_bool()
        terminal_font = buffer.read_bool()
        constant_width = buffer.read_bool()
        ink_inside = buffer.read_bool()
        ink_metrics = buffer.read_bool()
        draw_right_to_left = buffer.read_bool()
        buffer.skip(1)
        font_ascent = buffer.read_int32(is_ms_byte)
        font_descent = buffer.read_int32(is_ms_byte)
        max_overlap = buffer.read_int32(is_ms_byte)

        min_bounds = PcfMetric.parse(buffer, is_ms_byte, False)
        max_bounds = PcfMetric.parse(buffer, is_ms_byte, False)

        if has_ink_bounds:
            ink_min_bounds = PcfMetric.parse(buffer, is_ms_byte, False)
            ink_max_bounds = PcfMetric.parse(buffer, is_ms_byte, False)
        else:
            ink_min_bounds = None
            ink_max_bounds = None

        # TODO
        if header.table_size > buffer.tell() - header.table_offset:
            buffer.seek(header.table_offset + 4 + 8 + 4 * 3 + 2 * 6 * 2)
            _compat_chunk_start = buffer.tell() - header.table_offset
            _compat_chunk_size = header.table_size - _compat_chunk_start
            _compat_chunk = buffer.read(_compat_chunk_size)
            _compat_info = _compat_chunk_start, _compat_chunk_size, _compat_chunk
        else:
            _compat_info = None

        return PcfAccelerators(
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
            _compat_info,
        )

    def __init__(
            self,
            table_format: int = PcfTableFormat.build_for_accelerators(),
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
            min_bounds: PcfMetric = None,
            max_bounds: PcfMetric = None,
            ink_min_bounds: PcfMetric = None,
            ink_max_bounds: PcfMetric = None,
            _compat_info: tuple[int, int, bytes] = None,
    ):
        super().__init__(table_format)
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
        self._compat_info = _compat_info

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        is_ms_byte = PcfTableFormat.is_ms_byte(self.table_format)
        has_ink_bounds = PcfTableFormat.has_ink_bounds(self.table_format)

        buffer.seek(table_offset)
        buffer.write_int32(self.table_format)
        buffer.write_bool(self.no_overlap)
        buffer.write_bool(self.constant_metrics)
        buffer.write_bool(self.terminal_font)
        buffer.write_bool(self.constant_width)
        buffer.write_bool(self.ink_inside)
        buffer.write_bool(self.ink_metrics)
        buffer.write_bool(self.draw_right_to_left)
        buffer.write_nulls(1)
        buffer.write_int32(self.font_ascent, is_ms_byte)
        buffer.write_int32(self.font_descent, is_ms_byte)
        buffer.write_int32(self.max_overlap, is_ms_byte)

        self.min_bounds.dump(buffer, is_ms_byte, False)
        self.max_bounds.dump(buffer, is_ms_byte, False)

        if has_ink_bounds:
            self.ink_min_bounds.dump(buffer, is_ms_byte, False)
            self.ink_max_bounds.dump(buffer, is_ms_byte, False)

        table_size = buffer.tell() - table_offset

        # TODO
        if compat_mode and self._compat_info is not None:
            _compat_chunk_start, _compat_chunk_size, _compat_chunk = self._compat_info
            _compat_chunk = bytearray(_compat_chunk)

            ink_chunk_size = 2 * 6 * 2
            if table_size == _compat_chunk_start + ink_chunk_size:
                _compat_chunk_start += ink_chunk_size
                _compat_chunk_size -= ink_chunk_size
                for _ in range(ink_chunk_size):
                    if len(_compat_chunk) == 0:
                        break
                    _compat_chunk.pop(0)
            else:
                assert table_size == _compat_chunk_start

            buffer.write(_compat_chunk)
            table_size += _compat_chunk_size

        return table_size
