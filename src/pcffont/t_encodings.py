from collections import UserList

from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


# TODO
class PcfBdfEncodings(PcfTable, UserList[int]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfBdfEncodings':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)

        min_char_or_byte2 = buffer.read_int16(byte_order)
        max_char_or_byte2 = buffer.read_int16(byte_order)
        min_byte1 = buffer.read_int16(byte_order)
        max_byte1 = buffer.read_int16(byte_order)
        default_char = buffer.read_int16(byte_order)

        glyph_indices_count = (max_char_or_byte2 - min_char_or_byte2 + 1) * (max_byte1 - min_byte1 + 1)
        glyph_indices = [buffer.read_int16(byte_order) for _ in range(glyph_indices_count)]

        # TODO
        obj = PcfBdfEncodings(table_format, glyph_indices, default_char)
        buffer.seek(header.table_offset)
        obj.chuck = buffer.read(header.table_size)
        return obj

    def __init__(
            self,
            table_format: int = 0b1110,
            glyph_indices: list[int] = None,
            default_char: int = -1,
    ):
        PcfTable.__init__(self, table_format)
        UserList.__init__(self, glyph_indices)
        self.default_char = default_char

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        # TODO
        buffer.seek(table_offset)
        return buffer.write(self.chuck)
