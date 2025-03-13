from typing import Any

from pcffont.internal.stream import Stream


class PcfMetric:
    @staticmethod
    def parse(stream: Stream, ms_byte_first: bool, compressed: bool) -> 'PcfMetric':
        if compressed:
            left_side_bearing = stream.read_uint8() - 0x80
            right_side_bearing = stream.read_uint8() - 0x80
            character_width = stream.read_uint8() - 0x80
            ascent = stream.read_uint8() - 0x80
            descent = stream.read_uint8() - 0x80
            attributes = 0
        else:
            left_side_bearing = stream.read_int16(ms_byte_first)
            right_side_bearing = stream.read_int16(ms_byte_first)
            character_width = stream.read_int16(ms_byte_first)
            ascent = stream.read_int16(ms_byte_first)
            descent = stream.read_int16(ms_byte_first)
            attributes = stream.read_uint16(ms_byte_first)
        return PcfMetric(
            left_side_bearing,
            right_side_bearing,
            character_width,
            ascent,
            descent,
            attributes,
        )

    left_side_bearing: int
    right_side_bearing: int
    character_width: int
    ascent: int
    descent: int
    attributes: int

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
        return (f'PcfMetric('
                f'left_side_bearing={self.left_side_bearing!r}, '
                f'right_side_bearing={self.right_side_bearing!r}, '
                f'character_width={self.character_width!r}, '
                f'ascent={self.ascent!r}, '
                f'descent={self.descent!r}, '
                f'attributes={self.attributes!r}'
                f')')

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
    def offset_x(self) -> int:
        return self.left_side_bearing

    @property
    def offset_y(self) -> int:
        return -self.descent

    @property
    def offset(self) -> tuple[int, int]:
        return self.offset_x, self.offset_y

    @property
    def compressible(self) -> bool:
        return (-128 <= self.left_side_bearing <= 127 and
                -128 <= self.right_side_bearing <= 127 and
                -128 <= self.character_width <= 127 and
                -128 <= self.ascent <= 127 and
                -128 <= self.descent <= 127)

    def dump(self, stream: Stream, ms_byte_first: bool, compressed: bool):
        if compressed:
            stream.write_uint8(self.left_side_bearing + 0x80)
            stream.write_uint8(self.right_side_bearing + 0x80)
            stream.write_uint8(self.character_width + 0x80)
            stream.write_uint8(self.ascent + 0x80)
            stream.write_uint8(self.descent + 0x80)
        else:
            stream.write_int16(self.left_side_bearing, ms_byte_first)
            stream.write_int16(self.right_side_bearing, ms_byte_first)
            stream.write_int16(self.character_width, ms_byte_first)
            stream.write_int16(self.ascent, ms_byte_first)
            stream.write_int16(self.descent, ms_byte_first)
            stream.write_uint16(self.attributes, ms_byte_first)
