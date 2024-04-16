from pcffont.internal.buffer import Buffer


class PcfMetric:
    @staticmethod
    def parse(buffer: Buffer, is_ms_byte: bool, is_compressed: bool) -> 'PcfMetric':
        if is_compressed:
            left_side_bearing = buffer.read_int8() - 0x80
            right_side_bearing = buffer.read_int8() - 0x80
            character_width = buffer.read_int8() - 0x80
            ascent = buffer.read_int8() - 0x80
            descent = buffer.read_int8() - 0x80
            attributes = 0
        else:
            left_side_bearing = buffer.read_int16(is_ms_byte)
            right_side_bearing = buffer.read_int16(is_ms_byte)
            character_width = buffer.read_int16(is_ms_byte)
            ascent = buffer.read_int16(is_ms_byte)
            descent = buffer.read_int16(is_ms_byte)
            attributes = buffer.read_int16(is_ms_byte)
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

    @property
    def glyph_width(self) -> int:
        return self.right_side_bearing - self.left_side_bearing

    @property
    def glyph_height(self) -> int:
        return self.ascent + self.descent

    def dump(self, buffer: Buffer, is_ms_byte: bool, is_compressed: bool):
        if is_compressed:
            buffer.write_int8(self.left_side_bearing + 0x80)
            buffer.write_int8(self.right_side_bearing + 0x80)
            buffer.write_int8(self.character_width + 0x80)
            buffer.write_int8(self.ascent + 0x80)
            buffer.write_int8(self.descent + 0x80)
        else:
            buffer.write_int16(self.left_side_bearing, is_ms_byte)
            buffer.write_int16(self.right_side_bearing, is_ms_byte)
            buffer.write_int16(self.character_width, is_ms_byte)
            buffer.write_int16(self.ascent, is_ms_byte)
            buffer.write_int16(self.descent, is_ms_byte)
            buffer.write_int16(self.attributes, is_ms_byte)
