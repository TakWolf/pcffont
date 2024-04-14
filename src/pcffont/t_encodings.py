from collections import UserDict

from pcffont.error import PcfError
from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable

_NO_GLYPH_INDEX = 0xFFFF


class PcfBdfEncodings(PcfTable, UserDict[int, int]):
    """
    code_point -> glyph_index
    """

    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader, _strict_level: int) -> 'PcfBdfEncodings':
        table_format = util.read_and_check_table_format(buffer, header)
        is_ms_byte = util.is_ms_byte(table_format)

        first_col = buffer.read_int16(is_ms_byte)
        last_col = buffer.read_int16(is_ms_byte)
        first_row = buffer.read_int16(is_ms_byte)
        last_row = buffer.read_int16(is_ms_byte)
        default_char = buffer.read_int16(is_ms_byte)

        glyphs_count = (last_col - first_col + 1) * (last_row - first_row + 1)
        glyph_indices = [buffer.read_int16(is_ms_byte) for _ in range(glyphs_count)]

        mapping = {}
        if first_row == last_row == 0:
            for code_point in range(first_col, last_col + 1):
                glyph_index = glyph_indices[code_point - first_col]
                mapping[code_point] = glyph_index
        else:
            for row in range(first_row, last_row + 1):
                for col in range(first_col, last_col + 1):
                    code_point = int.from_bytes(bytes([row, col]))
                    glyph_index = glyph_indices[(row - first_row) * (last_col - first_col + 1) + col - first_col]
                    mapping[code_point] = glyph_index

        return PcfBdfEncodings(table_format, mapping, default_char)

    def __init__(
            self,
            table_format: int = PcfTable.DEFAULT_TABLE_FORMAT,
            mapping: dict[int, int] = None,
            default_char: int = -1,
    ):
        PcfTable.__init__(self, table_format)
        UserDict.__init__(self, mapping)
        self.default_char = default_char

    def __setitem__(self, code_point: int, glyph_index: int | None):
        if code_point < 0 or code_point > 0xFFFF:
            raise PcfError(f'Code point must between [0, 0xFFFF]')
        if glyph_index < 0 or glyph_index > _NO_GLYPH_INDEX:
            raise PcfError(f'Glyph index must between [0, 0x{_NO_GLYPH_INDEX:04X}]')

        if glyph_index == _NO_GLYPH_INDEX:
            glyph_index = None

        if glyph_index is None:
            self.pop(code_point, None)
        else:
            super().__setitem__(code_point, glyph_index)

    def _dump(self, buffer: Buffer, table_offset: int, compat_mode: bool = False) -> int:
        is_ms_byte = util.is_ms_byte(self.table_format)

        max_code_point = max(self)
        if max_code_point <= 0xFF:
            first_col = min(self)
            last_col = max_code_point
            first_row = 0
            last_row = 0
        else:
            first_col = 0
            last_col = 0xFF
            first_row = 0
            last_row = 0xFF

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
