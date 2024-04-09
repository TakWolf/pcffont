from collections import UserList

from pcffont.header import PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.table import PcfTable


class PcfBdfEncodings(PcfTable, UserList[int]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfBdfEncodings':
        _, byte_order = header.read_and_check_table_format(buffer)

        min_char_or_byte2 = buffer.read_int16(byte_order)
        max_char_or_byte2 = buffer.read_int16(byte_order)
        min_byte1 = buffer.read_int16(byte_order)
        max_byte1 = buffer.read_int16(byte_order)
        default_char = buffer.read_int16(byte_order)

        glyph_indices_count = (max_char_or_byte2 - min_char_or_byte2 + 1) * (max_byte1 - min_byte1 + 1)
        glyph_indices = [buffer.read_int16(byte_order) for _ in range(glyph_indices_count)]

        return PcfBdfEncodings(glyph_indices, default_char)

    def __init__(self, glyph_indices: list[int] = None, default_char: int = -1):
        super().__init__(glyph_indices)
        self.default_char = default_char

    def _dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        pass
