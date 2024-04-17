from pcffont.internal.buffer import Buffer


class PcfMetric:
    @staticmethod
    def parse(buffer: Buffer, ms_byte_first: bool, is_compressed: bool) -> 'PcfMetric':
        if is_compressed:
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

    @property
    def glyph_width(self) -> int:
        return self.right_side_bearing - self.left_side_bearing

    @property
    def glyph_height(self) -> int:
        return self.ascent + self.descent

    def dump(self, buffer: Buffer, ms_byte_first: bool, is_compressed: bool):
        if is_compressed:
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
