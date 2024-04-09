import os
from collections import UserDict
from typing import BinaryIO

from pcffont import table_registry
from pcffont.error import PcfError
from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.t_glyph_names import PcfGlyphNames
from pcffont.t_properties import PcfProperties
from pcffont.t_scalable_widths import PcfScalableWidths
from pcffont.table import PcfTable

_MAGIC_STRING = b'\x01fcp'


class PcfFont(UserDict[PcfTableType, PcfTable]):
    @staticmethod
    def parse(stream: BinaryIO) -> 'PcfFont':
        buffer = Buffer(stream)

        buffer.seek(0)
        if buffer.read(4) != _MAGIC_STRING:
            raise PcfError('Not PCF format')

        headers = PcfHeader.parse(buffer)
        tables = {table_type: table_registry.parse(buffer, header) for table_type, header in headers.items()}

        return PcfFont(tables)

    @staticmethod
    def load(file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> 'PcfFont':
        with open(file_path, 'rb') as file:
            return PcfFont.parse(file)

    def __init__(self, tables: dict[PcfTableType, PcfTable | None] = None):
        super().__init__(tables)

    def __setitem__(self, table_type: PcfTableType, table: PcfTable | None):
        if table is None:
            self.pop(table_type, None)
        else:
            assert table_type == table.table_type
            super().__setitem__(table_type, table)

    @property
    def properties(self) -> PcfProperties | None:
        return self.get(PcfTableType.PROPERTIES, None)

    @properties.setter
    def properties(self, table: PcfProperties | None):
        self[PcfTableType.PROPERTIES] = table

    @property
    def scalable_widths(self) -> PcfScalableWidths | None:
        return self.get(PcfTableType.SWIDTHS, None)

    @scalable_widths.setter
    def scalable_widths(self, table: PcfScalableWidths | None):
        self[PcfTableType.SWIDTHS] = table

    @property
    def glyph_names(self) -> PcfGlyphNames | None:
        return self.get(PcfTableType.GLYPH_NAMES, None)

    @glyph_names.setter
    def glyph_names(self, table: PcfGlyphNames | None):
        self[PcfTableType.GLYPH_NAMES] = table

    def dump(self, stream: BinaryIO):
        buffer = Buffer(stream)

        headers = []
        table_offset = 8 + 16 * len(self)
        for table in self.values():
            table_format, table_size = table.dump(buffer, table_offset)
            headers.append(PcfHeader(table.table_type, table_format, table_size, table_offset))
            table_offset += table_size

        buffer.seek(0)
        buffer.write(_MAGIC_STRING)
        buffer.write_int_le(len(self))
        for header in headers:
            header.dump(buffer)

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        with open(file_path, 'wb') as file:
            self.dump(file)
