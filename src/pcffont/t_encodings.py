from collections import UserDict

from pcffont.error import PcfOutOfRangeError
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable

_MAX_CODE_POINT = 0xFFFF
_NO_GLYPH_INDEX = 0xFFFF


class PcfBdfEncodings(PcfTable, UserDict[int, int]):
    """
    code_point -> glyph_index
    """

    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfBdfEncodings':
        table_format = PcfTableFormat.read_and_check(buffer, header)
        is_ms_byte = PcfTableFormat.is_ms_byte(table_format)

        min_byte_2 = buffer.read_uint16(is_ms_byte)
        max_byte_2 = buffer.read_uint16(is_ms_byte)
        min_byte_1 = buffer.read_uint16(is_ms_byte)
        max_byte_1 = buffer.read_uint16(is_ms_byte)
        default_char = buffer.read_uint16(is_ms_byte)

        glyphs_count = (max_byte_2 - min_byte_2 + 1) * (max_byte_1 - min_byte_1 + 1)
        glyph_indices = [buffer.read_uint16(is_ms_byte) for _ in range(glyphs_count)]

        encodings = PcfBdfEncodings(table_format, default_char)
        if min_byte_1 == max_byte_1 == 0:
            for code_point in range(min_byte_2, max_byte_2 + 1):
                glyph_index = glyph_indices[code_point - min_byte_2]
                encodings[code_point] = glyph_index
        else:
            for byte_1 in range(min_byte_1, max_byte_1 + 1):
                for byte_2 in range(min_byte_2, max_byte_2 + 1):
                    code_point = int.from_bytes(bytes([byte_1, byte_2]))
                    glyph_index = glyph_indices[(byte_1 - min_byte_1) * (max_byte_2 - min_byte_2 + 1) + byte_2 - min_byte_2]
                    encodings[code_point] = glyph_index
        return encodings

    def __init__(
            self,
            table_format: int = PcfTableFormat.build(),
            default_char: int = _NO_GLYPH_INDEX,
            encodings: dict[int, int] = None,
    ):
        PcfTable.__init__(self, table_format)
        UserDict.__init__(self, encodings)
        self.default_char = default_char

    def __setitem__(self, code_point: int, glyph_index: int | None):
        if code_point < 0 or code_point > _MAX_CODE_POINT:
            raise PcfOutOfRangeError(f'Code point must between [0, {_MAX_CODE_POINT}]')
        if glyph_index < 0 or glyph_index > _NO_GLYPH_INDEX:
            raise PcfOutOfRangeError(f'Glyph index must between [0, {_NO_GLYPH_INDEX}]')

        if glyph_index is None or glyph_index == _NO_GLYPH_INDEX:
            self.pop(code_point, None)
        else:
            super().__setitem__(code_point, glyph_index)

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        is_ms_byte = PcfTableFormat.is_ms_byte(self.table_format)

        min_byte_2 = 0xFF
        max_byte_2 = 0
        min_byte_1 = 0xFF
        max_byte_1 = 0
        for code_point in self:
            bs = code_point.to_bytes(2)
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
        buffer.write_int32(self.table_format)
        buffer.write_uint16(min_byte_2, is_ms_byte)
        buffer.write_uint16(max_byte_2, is_ms_byte)
        buffer.write_uint16(min_byte_1, is_ms_byte)
        buffer.write_uint16(max_byte_1, is_ms_byte)
        buffer.write_uint16(self.default_char, is_ms_byte)

        if min_byte_1 == max_byte_1 == 0:
            for code_point in range(min_byte_2, max_byte_2 + 1):
                glyph_index = self.get(code_point, _NO_GLYPH_INDEX)
                buffer.write_uint16(glyph_index, is_ms_byte)
        else:
            for byte_1 in range(min_byte_1, max_byte_1 + 1):
                for byte_2 in range(min_byte_2, max_byte_2 + 1):
                    code_point = int.from_bytes(bytes([byte_1, byte_2]))
                    glyph_index = self.get(code_point, _NO_GLYPH_INDEX)
                    buffer.write_uint16(glyph_index, is_ms_byte)

        table_size = buffer.tell() - table_offset
        return table_size
