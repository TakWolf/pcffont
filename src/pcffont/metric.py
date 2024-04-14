from pcffont.internal.buffer import ByteOrder, Buffer


class PcfMetric:
    @staticmethod
    def parse(buffer: Buffer, byte_order: ByteOrder, is_compressed: bool) -> 'PcfMetric':
        if is_compressed:
            left_side_bearing = buffer.read_int8(byte_order) - 0x80
            right_side_bearing = buffer.read_int8(byte_order) - 0x80
            character_width = buffer.read_int8(byte_order) - 0x80
            ascent = buffer.read_int8(byte_order) - 0x80
            descent = buffer.read_int8(byte_order) - 0x80
            attributes = 0
        else:
            left_side_bearing = buffer.read_int16(byte_order)
            right_side_bearing = buffer.read_int16(byte_order)
            character_width = buffer.read_int16(byte_order)
            ascent = buffer.read_int16(byte_order)
            descent = buffer.read_int16(byte_order)
            attributes = buffer.read_int16(byte_order)
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

    def dump(self, buffer: Buffer, byte_order: ByteOrder, is_compressed: bool):
        if is_compressed:
            buffer.write_int8(self.left_side_bearing + 0x80, byte_order)
            buffer.write_int8(self.right_side_bearing + 0x80, byte_order)
            buffer.write_int8(self.character_width + 0x80, byte_order)
            buffer.write_int8(self.ascent + 0x80, byte_order)
            buffer.write_int8(self.descent + 0x80, byte_order)
        else:
            buffer.write_int16(self.left_side_bearing, byte_order)
            buffer.write_int16(self.right_side_bearing, byte_order)
            buffer.write_int16(self.character_width, byte_order)
            buffer.write_int16(self.ascent, byte_order)
            buffer.write_int16(self.descent, byte_order)
            buffer.write_int16(self.attributes, byte_order)
