from collections import UserDict
from typing import Final, Any

import pcffont
from pcffont.error import PcfOutOfRangeError
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


class PcfBdfEncodings(PcfTable, UserDict[int, int]):
    """
    code_point -> glyph_index
    """

    MAX_CODE_POINT: Final[int] = 0xFFFF
    NO_GLYPH_INDEX: Final[int] = 0xFFFF

    @staticmethod
    def parse(buffer: Buffer, _font: 'pcffont.PcfFont', header: PcfHeader, strict_level: int) -> 'PcfBdfEncodings':
        table_format = header.read_and_check_table_format(buffer, strict_level)

        min_byte_2 = buffer.read_uint16(table_format.ms_byte_first)
        max_byte_2 = buffer.read_uint16(table_format.ms_byte_first)
        min_byte_1 = buffer.read_uint16(table_format.ms_byte_first)
        max_byte_1 = buffer.read_uint16(table_format.ms_byte_first)
        default_char = buffer.read_uint16(table_format.ms_byte_first)

        glyphs_count = (max_byte_2 - min_byte_2 + 1) * (max_byte_1 - min_byte_1 + 1)
        glyph_indices = buffer.read_uint16_list(glyphs_count, table_format.ms_byte_first)

        encodings = PcfBdfEncodings(table_format, default_char)
        if min_byte_1 == max_byte_1 == 0:
            for code_point in range(min_byte_2, max_byte_2 + 1):
                glyph_index = glyph_indices[code_point - min_byte_2]
                encodings[code_point] = glyph_index
        else:
            for byte_1 in range(min_byte_1, max_byte_1 + 1):
                for byte_2 in range(min_byte_2, max_byte_2 + 1):
                    code_point = int.from_bytes(bytes([byte_1, byte_2]), 'big')
                    glyph_index = glyph_indices[(byte_1 - min_byte_1) * (max_byte_2 - min_byte_2 + 1) + byte_2 - min_byte_2]
                    encodings[code_point] = glyph_index
        return encodings

    def __init__(
            self,
            table_format: PcfTableFormat = None,
            default_char: int = NO_GLYPH_INDEX,
            encodings: dict[int, int] = None,
    ):
        if table_format is None:
            table_format = PcfTableFormat()
        PcfTable.__init__(self, table_format)
        UserDict.__init__(self, encodings)
        self.default_char = default_char

    def __setitem__(self, code_point: int, glyph_index: int | None):
        if code_point < 0 or code_point > PcfBdfEncodings.MAX_CODE_POINT:
            raise PcfOutOfRangeError(f'Code point must between [0, {PcfBdfEncodings.MAX_CODE_POINT}]')
        if glyph_index < 0 or glyph_index > PcfBdfEncodings.NO_GLYPH_INDEX:
            raise PcfOutOfRangeError(f'Glyph index must between [0, {PcfBdfEncodings.NO_GLYPH_INDEX}]')

        if glyph_index is None or glyph_index == PcfBdfEncodings.NO_GLYPH_INDEX:
            self.pop(code_point, None)
        else:
            super().__setitem__(code_point, glyph_index)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfBdfEncodings):
            return False
        return (self.table_format == other.table_format and
                self.default_char == other.default_char and
                UserDict.__eq__(self, other))

    def _dump(self, buffer: Buffer, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        min_byte_2 = 0xFF
        max_byte_2 = 0
        min_byte_1 = 0xFF
        max_byte_1 = 0
        for code_point in self:
            bs = code_point.to_bytes(2, 'big')
            byte_1 = bs[0]
            byte_2 = bs[1]
            if byte_1 < min_byte_1:
                min_byte_1 = byte_1
            if byte_1 > max_byte_1:
                max_byte_1 = byte_1
            if byte_2 < min_byte_2:
                min_byte_2 = byte_2
            if byte_2 > max_byte_2:
                max_byte_2 = byte_2

        buffer.seek(table_offset)
        buffer.write_uint32(self.table_format.value)
        buffer.write_uint16(min_byte_2, self.table_format.ms_byte_first)
        buffer.write_uint16(max_byte_2, self.table_format.ms_byte_first)
        buffer.write_uint16(min_byte_1, self.table_format.ms_byte_first)
        buffer.write_uint16(max_byte_1, self.table_format.ms_byte_first)
        buffer.write_uint16(self.default_char, self.table_format.ms_byte_first)

        if min_byte_1 == max_byte_1 == 0:
            for code_point in range(min_byte_2, max_byte_2 + 1):
                glyph_index = self.get(code_point, PcfBdfEncodings.NO_GLYPH_INDEX)
                buffer.write_uint16(glyph_index, self.table_format.ms_byte_first)
        else:
            for byte_1 in range(min_byte_1, max_byte_1 + 1):
                for byte_2 in range(min_byte_2, max_byte_2 + 1):
                    code_point = int.from_bytes(bytes([byte_1, byte_2]), 'big')
                    glyph_index = self.get(code_point, PcfBdfEncodings.NO_GLYPH_INDEX)
                    buffer.write_uint16(glyph_index, self.table_format.ms_byte_first)

        table_size = buffer.tell() - table_offset
        return table_size
