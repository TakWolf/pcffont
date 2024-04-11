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

        mapping = {}
        if min_byte1 == max_byte1 == 0:
            for code_point in range(min_char_or_byte2, max_char_or_byte2 + 1):
                glyph_index = glyph_indices[code_point - min_char_or_byte2]
                mapping[code_point] = glyph_index
        else:
            for enc1 in range(min_byte1, max_byte1 + 1):
                for enc2 in range(min_char_or_byte2, max_char_or_byte2 + 1):
                    code_point = int.from_bytes(bytes([enc1, enc2]))
                    glyph_index = glyph_indices[(enc1 - min_byte1) * (max_char_or_byte2 - min_char_or_byte2 + 1) + enc2 - min_char_or_byte2]
                    mapping[code_point] = glyph_index

        return PcfBdfEncodings(table_format, mapping, default_char)

    def __init__(
            self,
            table_format: int = PcfTable.DEFAULT_TABLE_FORMAT,
            mapping: dict[int, int] = None,
            default_char: int = _NO_GLYPH_INDEX,
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
        byte_order = util.get_table_byte_order(self.table_format)

        max_code_point = max(self)
        if max_code_point <= 0xFF:
            min_char_or_byte2 = min(self)
            max_char_or_byte2 = max_code_point
            min_byte1 = 0
            max_byte1 = 0
        else:
            min_char_or_byte2 = 0
            max_char_or_byte2 = 0xFF
            min_byte1 = 0
            max_byte1 = 0xFF

        buffer.seek(table_offset)
        buffer.write_int32_le(self.table_format)
        buffer.write_int16(min_char_or_byte2, byte_order)
        buffer.write_int16(max_char_or_byte2, byte_order)
        buffer.write_int16(min_byte1, byte_order)
        buffer.write_int16(max_byte1, byte_order)
        buffer.write_int16(self.default_char, byte_order)

        if min_byte1 == max_byte1 == 0:
            for code_point in range(min_char_or_byte2, max_char_or_byte2 + 1):
                glyph_index = self.get(code_point, _NO_GLYPH_INDEX)
                buffer.write_int16(glyph_index, byte_order)
        else:
            for enc1 in range(min_byte1, max_byte1 + 1):
                for enc2 in range(min_char_or_byte2, max_char_or_byte2 + 1):
                    code_point = int.from_bytes(bytes([enc1, enc2]))
                    glyph_index = self.get(code_point, _NO_GLYPH_INDEX)
                    buffer.write_int16(glyph_index, byte_order)

        table_size = buffer.tell() - table_offset
        return table_size
