from pcffont.header import PcfTableFormat, PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.metric import PcfMetric
from pcffont.table import PcfTable


class PcfAccelerators(PcfTable):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfAccelerators':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)
        is_accel_w_ink_bounds = table_format & PcfTableFormat.ACCEL_W_INKBOUNDS

        no_overlap = buffer.read_bool()
        constant_metrics = buffer.read_bool()
        terminal_font = buffer.read_bool()
        constant_width = buffer.read_bool()
        ink_inside = buffer.read_bool()
        ink_metrics = buffer.read_bool()
        draw_direction_right_to_left = buffer.read_bool()
        buffer.skip(1)
        font_ascent = buffer.read_int32(byte_order)
        font_descent = buffer.read_int32(byte_order)
        max_overlap = buffer.read_int32(byte_order)

        min_bounds = PcfMetric.parse(buffer, byte_order, False)
        max_bounds = PcfMetric.parse(buffer, byte_order, False)

        if is_accel_w_ink_bounds:
            ink_min_bounds = PcfMetric.parse(buffer, byte_order, False)
            ink_max_bounds = PcfMetric.parse(buffer, byte_order, False)
        else:
            ink_min_bounds = None
            ink_max_bounds = None

        return PcfAccelerators(
            table_format,
            no_overlap,
            constant_metrics,
            terminal_font,
            constant_width,
            ink_inside,
            ink_metrics,
            draw_direction_right_to_left,
            font_ascent,
            font_descent,
            max_overlap,
            min_bounds,
            max_bounds,
            ink_min_bounds,
            ink_max_bounds,
        )

    def __init__(
            self,
            table_format: int = 0b1110,
            no_overlap: bool = False,
            constant_metrics: bool = False,
            terminal_font: bool = False,
            constant_width: bool = False,
            ink_inside: bool = False,
            ink_metrics: bool = False,
            draw_direction_right_to_left: bool = False,
            font_ascent: int = 0,
            font_descent: int = 0,
            max_overlap: int = 0,
            min_bounds: PcfMetric = None,
            max_bounds: PcfMetric = None,
            ink_min_bounds: PcfMetric = None,
            ink_max_bounds: PcfMetric = None,
    ):
        super().__init__(table_format)
        self.no_overlap = no_overlap
        self.constant_metrics = constant_metrics
        self.terminal_font = terminal_font
        self.constant_width = constant_width
        self.ink_inside = ink_inside
        self.ink_metrics = ink_metrics
        self.draw_direction_right_to_left = draw_direction_right_to_left
        self.font_ascent = font_ascent
        self.font_descent = font_descent
        self.max_overlap = max_overlap
        self.min_bounds = min_bounds
        self.max_bounds = max_bounds
        self.ink_min_bounds = ink_min_bounds
        self.ink_max_bounds = ink_max_bounds

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        byte_order = util.get_table_byte_order(self.table_format)
        is_accel_w_ink_bounds = self.table_format & PcfTableFormat.ACCEL_W_INKBOUNDS

        table_size = 4 + 8 + 4 * 3 + 2 * 6
        if is_accel_w_ink_bounds:
            table_size += 2 * 6

        buffer.seek(table_offset)
        buffer.write_int32_le(self.table_format)
        buffer.write_bool(self.no_overlap)
        buffer.write_bool(self.constant_metrics)
        buffer.write_bool(self.terminal_font)
        buffer.write_bool(self.constant_width)
        buffer.write_bool(self.ink_inside)
        buffer.write_bool(self.ink_metrics)
        buffer.write_bool(self.draw_direction_right_to_left)
        buffer.write_nulls(1)
        buffer.write_int32(self.font_ascent, byte_order)
        buffer.write_int32(self.font_descent, byte_order)
        buffer.write_int32(self.max_overlap, byte_order)

        self.min_bounds.dump(buffer, byte_order, False)
        self.max_bounds.dump(buffer, byte_order, False)

        if is_accel_w_ink_bounds:
            self.ink_min_bounds.dump(buffer, byte_order, False)
            self.ink_max_bounds.dump(buffer, byte_order, False)

        return table_size