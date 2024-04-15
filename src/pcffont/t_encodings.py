from collections import UserDict

from pcffont.error import PcfError
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

        first_col = buffer.read_int16(is_ms_byte)
        last_col = buffer.read_int16(is_ms_byte)
        first_row = buffer.read_int16(is_ms_byte)
        last_row = buffer.read_int16(is_ms_byte)
        default_char = buffer.read_int16(is_ms_byte)

        glyphs_count = (last_col - first_col + 1) * (last_row - first_row + 1)
        glyph_indices = [buffer.read_int16(is_ms_byte) for _ in range(glyphs_count)]

        encodings = PcfBdfEncodings(table_format, default_char)
        if first_row == last_row == 0:
            for code_point in range(first_col, last_col + 1):
                glyph_index = glyph_indices[code_point - first_col]
                encodings[code_point] = glyph_index
        else:
            for row in range(first_row, last_row + 1):
                for col in range(first_col, last_col + 1):
                    code_point = int.from_bytes(bytes([row, col]))
                    glyph_index = glyph_indices[(row - first_row) * (last_col - first_col + 1) + col - first_col]
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
            raise PcfError(f'Code point must between [0, {_MAX_CODE_POINT}]')
        if glyph_index < 0 or glyph_index > _NO_GLYPH_INDEX:
            raise PcfError(f'Glyph index must between [0, {_NO_GLYPH_INDEX}]')

        if glyph_index == _NO_GLYPH_INDEX:
            glyph_index = None

        if glyph_index is None:
            self.pop(code_point, None)
        else:
            super().__setitem__(code_point, glyph_index)

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        is_ms_byte = PcfTableFormat.is_ms_byte(self.table_format)

        first_col = 0xFF
        last_col = 0
        first_row = 0xFF
        last_row = 0
        for code_point in self:
            bs = code_point.to_bytes(2)
            row = bs[0]
            col = bs[1]
            if row < first_row:
                first_row = row
            if row > last_row:
                last_row = row
            if col < first_col:
                first_col = col
            if col > last_col:
                last_col = col

        buffer.seek(table_offset)
        buffer.write_int32(self.table_format)
        buffer.write_int16(first_col, is_ms_byte)
        buffer.write_int16(last_col, is_ms_byte)
        buffer.write_int16(first_row, is_ms_byte)
        buffer.write_int16(last_row, is_ms_byte)
        buffer.write_int16(self.default_char, is_ms_byte)

        if first_row == last_row == 0:
            for code_point in range(first_col, last_col + 1):
                glyph_index = self.get(code_point, _NO_GLYPH_INDEX)
                buffer.write_int16(glyph_index, is_ms_byte)
        else:
            for row in range(first_row, last_row + 1):
                for col in range(first_col, last_col + 1):
                    code_point = int.from_bytes(bytes([row, col]))
                    glyph_index = self.get(code_point, _NO_GLYPH_INDEX)
                    buffer.write_int16(glyph_index, is_ms_byte)

        table_size = buffer.tell() - table_offset
        return table_size
