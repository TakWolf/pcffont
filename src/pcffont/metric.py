from pcffont.internal.buffer import ByteOrder, Buffer


class PcfMetric:
    @staticmethod
    def parse(buffer: Buffer, byte_order: ByteOrder, is_compressed: bool) -> 'PcfMetric':
        if is_compressed:
            left_sided_bearing = buffer.read_int8(byte_order)
            right_side_bearing = buffer.read_int8(byte_order)
            character_width = buffer.read_int8(byte_order)
            character_ascent = buffer.read_int8(byte_order)
            character_descent = buffer.read_int8(byte_order)
            character_attributes = 0
        else:
            left_sided_bearing = buffer.read_int16(byte_order)
            right_side_bearing = buffer.read_int16(byte_order)
            character_width = buffer.read_int16(byte_order)
            character_ascent = buffer.read_int16(byte_order)
            character_descent = buffer.read_int16(byte_order)
            character_attributes = buffer.read_int16(byte_order)
        return PcfMetric(
            left_sided_bearing,
            right_side_bearing,
            character_width,
            character_ascent,
            character_descent,
            character_attributes,
        )

    def __init__(
            self,
            left_sided_bearing: int,
            right_side_bearing: int,
            character_width: int,
            character_ascent: int,
            character_descent: int,
            character_attributes: int = 0,
    ):
        self.left_sided_bearing = left_sided_bearing
        self.right_side_bearing = right_side_bearing
        self.character_width = character_width
        self.character_ascent = character_ascent
        self.character_descent = character_descent
        self.character_attributes = character_attributes

    def dump(self, buffer: Buffer, byte_order: ByteOrder, is_compressed: bool):
        if is_compressed:
            buffer.write_int8(self.left_sided_bearing, byte_order)
            buffer.write_int8(self.right_side_bearing, byte_order)
            buffer.write_int8(self.character_width, byte_order)
            buffer.write_int8(self.character_ascent, byte_order)
            buffer.write_int8(self.character_descent, byte_order)
        else:
            buffer.write_int16(self.left_sided_bearing, byte_order)
            buffer.write_int16(self.right_side_bearing, byte_order)
            buffer.write_int16(self.character_width, byte_order)
            buffer.write_int16(self.character_ascent, byte_order)
            buffer.write_int16(self.character_descent, byte_order)
            buffer.write_int16(self.character_attributes, byte_order)
