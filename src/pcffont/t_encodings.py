from collections import UserDict
from typing import Final, Any

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.stream import Stream


class PcfBdfEncodings(UserDict[int, int]):
    """
    encoding -> glyph_index
    """

    MAX_ENCODING: Final = 0xFFFF
    NO_GLYPH_INDEX: Final = 0xFFFF

    @staticmethod
    def parse(stream: Stream, _font: 'pcffont.PcfFont', header: PcfHeader) -> 'PcfBdfEncodings':
        table_format = header.read_and_check_table_format(stream)

        min_byte_2 = stream.read_uint16(table_format.ms_byte_first)
        max_byte_2 = stream.read_uint16(table_format.ms_byte_first)
        min_byte_1 = stream.read_uint16(table_format.ms_byte_first)
        max_byte_1 = stream.read_uint16(table_format.ms_byte_first)
        default_char = stream.read_uint16(table_format.ms_byte_first)

        glyphs_count = (max_byte_2 - min_byte_2 + 1) * (max_byte_1 - min_byte_1 + 1)
        glyph_indices = stream.read_uint16_list(glyphs_count, table_format.ms_byte_first)

        encodings = PcfBdfEncodings(table_format, default_char)
        if min_byte_1 == max_byte_1 == 0:
            for encoding in range(min_byte_2, max_byte_2 + 1):
                glyph_index = glyph_indices[encoding - min_byte_2]
                encodings[encoding] = glyph_index
        else:
            for byte_1 in range(min_byte_1, max_byte_1 + 1):
                for byte_2 in range(min_byte_2, max_byte_2 + 1):
                    encoding = int.from_bytes(bytes([byte_1, byte_2]), 'big')
                    glyph_index = glyph_indices[(byte_1 - min_byte_1) * (max_byte_2 - min_byte_2 + 1) + byte_2 - min_byte_2]
                    encodings[encoding] = glyph_index
        return encodings

    table_format: PcfTableFormat
    default_char: int

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            default_char: int = NO_GLYPH_INDEX,
            encodings: dict[int, int] | None = None,
    ):
        super().__init__(encodings)
        self.table_format = PcfTableFormat() if table_format is None else table_format
        self.default_char = default_char

    def __setitem__(self, encoding: Any, glyph_index: Any):
        if not isinstance(encoding, int):
            raise KeyError(f"expected type 'int', got '{type(encoding).__name__}' instead")

        if encoding < 0 or encoding > PcfBdfEncodings.MAX_ENCODING:
            raise KeyError(f'encoding must between [0, {PcfBdfEncodings.MAX_ENCODING}]')

        if glyph_index is None or glyph_index == PcfBdfEncodings.NO_GLYPH_INDEX:
            self.pop(encoding, None)
            return

        if not isinstance(glyph_index, int):
            raise ValueError(f"illegal value type: '{type(glyph_index).__name__}'")

        if glyph_index < 0 or glyph_index > PcfBdfEncodings.NO_GLYPH_INDEX:
            raise ValueError(f'glyph index must between [0, {PcfBdfEncodings.NO_GLYPH_INDEX}]')

        super().__setitem__(encoding, glyph_index)

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfBdfEncodings):
            return False
        return (self.table_format == other.table_format and
                self.default_char == other.default_char and
                super().__eq__(other))

    def dump(self, stream: Stream, _font: 'pcffont.PcfFont', table_offset: int) -> int:
        min_byte_2 = 0xFF
        max_byte_2 = 0
        min_byte_1 = 0xFF
        max_byte_1 = 0
        for encoding in self:
            bs = encoding.to_bytes(2, 'big')
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

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_uint16(min_byte_2, self.table_format.ms_byte_first)
        stream.write_uint16(max_byte_2, self.table_format.ms_byte_first)
        stream.write_uint16(min_byte_1, self.table_format.ms_byte_first)
        stream.write_uint16(max_byte_1, self.table_format.ms_byte_first)
        stream.write_uint16(self.default_char, self.table_format.ms_byte_first)

        if min_byte_1 == max_byte_1 == 0:
            for encoding in range(min_byte_2, max_byte_2 + 1):
                glyph_index = self.get(encoding, PcfBdfEncodings.NO_GLYPH_INDEX)
                stream.write_uint16(glyph_index, self.table_format.ms_byte_first)
        else:
            for byte_1 in range(min_byte_1, max_byte_1 + 1):
                for byte_2 in range(min_byte_2, max_byte_2 + 1):
                    encoding = int.from_bytes(bytes([byte_1, byte_2]), 'big')
                    glyph_index = self.get(encoding, PcfBdfEncodings.NO_GLYPH_INDEX)
                    stream.write_uint16(glyph_index, self.table_format.ms_byte_first)

        stream.align_to_bit32_with_nulls()

        table_size = stream.tell() - table_offset
        return table_size
