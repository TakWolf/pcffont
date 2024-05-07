from typing import Any

from pcffont.internal.buffer import Buffer


class PcfMetric:
    @staticmethod
    def parse(buffer: Buffer, ms_byte_first: bool, compressed: bool) -> 'PcfMetric':
        if compressed:
            left_side_bearing = buffer.read_uint8() - 0x80
            right_side_bearing = buffer.read_uint8() - 0x80
            character_width = buffer.read_uint8() - 0x80
            ascent = buffer.read_uint8() - 0x80
            descent = buffer.read_uint8() - 0x80
            attributes = 0
        else:
            left_side_bearing = buffer.read_int16(ms_byte_first)
            right_side_bearing = buffer.read_int16(ms_byte_first)
            character_width = buffer.read_int16(ms_byte_first)
            ascent = buffer.read_int16(ms_byte_first)
            descent = buffer.read_int16(ms_byte_first)
            attributes = buffer.read_uint16(ms_byte_first)
        return PcfMetric(
            left_side_bearing,
            right_side_bearing,
            character_width,
            ascent,
            descent,
            attributes,
        )

    def __init__(
            self,
            left_side_bearing: int,
            right_side_bearing: int,
            character_width: int,
            ascent: int,
            descent: int,
            attributes: int = 0,
    ):
        self.left_side_bearing = left_side_bearing
        self.right_side_bearing = right_side_bearing
        self.character_width = character_width
        self.ascent = ascent
        self.descent = descent
        self.attributes = attributes

    def __repr__(self) -> str:
        return (f'left_side_bearing: {self.left_side_bearing}, '
                f'right_side_bearing: {self.right_side_bearing}, '
                f'character_width: {self.character_width}, '
                f'ascent: {self.ascent}, '
                f'descent: {self.descent}, '
                f'attributes: {self.attributes}')

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfMetric):
            return False
        return (self.left_side_bearing == other.left_side_bearing and
                self.right_side_bearing == other.right_side_bearing and
                self.character_width == other.character_width and
                self.ascent == other.ascent and
                self.descent == other.descent and
                self.attributes == other.attributes)

    @property
    def width(self) -> int:
        return self.right_side_bearing - self.left_side_bearing

    @property
    def height(self) -> int:
        return self.ascent + self.descent

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def origin_x(self) -> int:
        return self.left_side_bearing

    @property
    def origin_y(self) -> int:
        return -self.descent

    @property
    def origin(self) -> tuple[int, int]:
        return self.origin_x, self.origin_y

    @property
    def compressible(self) -> bool:
        return (-128 <= self.left_side_bearing <= 127 and
                -128 <= self.right_side_bearing <= 127 and
                -128 <= self.character_width <= 127 and
                -128 <= self.ascent <= 127 and
                -128 <= self.descent <= 127)

    def dump(self, buffer: Buffer, ms_byte_first: bool, compressed: bool):
        if compressed:
            buffer.write_uint8(self.left_side_bearing + 0x80)
            buffer.write_uint8(self.right_side_bearing + 0x80)
            buffer.write_uint8(self.character_width + 0x80)
            buffer.write_uint8(self.ascent + 0x80)
            buffer.write_uint8(self.descent + 0x80)
        else:
            buffer.write_int16(self.left_side_bearing, ms_byte_first)
            buffer.write_int16(self.right_side_bearing, ms_byte_first)
            buffer.write_int16(self.character_width, ms_byte_first)
            buffer.write_int16(self.ascent, ms_byte_first)
            buffer.write_int16(self.descent, ms_byte_first)
            buffer.write_uint16(self.attributes, ms_byte_first)
