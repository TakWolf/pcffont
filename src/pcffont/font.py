import os
from typing import BinaryIO

from pcffont.error import PcfError
from pcffont.glyph_names import PcfGlyphNames
from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.properties import PcfProperties
from pcffont.table import PcfTable

_MAGIC_STRING = b'\x01fcp'


class PcfFont:
    @staticmethod
    def parse(stream: BinaryIO) -> 'PcfFont':
        buffer = Buffer(stream)

        buffer.seek(0)
        if buffer.read(4) != _MAGIC_STRING:
            raise PcfError('Not PCF format')

        headers = PcfHeader.parse(buffer)

        tables = {}
        for table_type, header in headers.items():
            if table_type == PcfTableType.PROPERTIES:
                tables[table_type] = PcfProperties.parse(buffer, header)
            elif table_type == PcfTableType.GLYPH_NAMES:
                tables[table_type] = PcfGlyphNames.parse(buffer, header)

        return PcfFont(tables)

    @staticmethod
    def load(file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> 'PcfFont':
        with open(file_path, 'rb') as file:
            return PcfFont.parse(file)

    def __init__(self, tables: dict[PcfTableType, PcfTable] = None):
        if tables is None:
            tables = {}
        self.tables = tables

    @property
    def properties(self) -> PcfProperties | None:
        return self.tables.get(PcfTableType.PROPERTIES, None)

    @properties.setter
    def properties(self, table: PcfProperties | None):
        self.tables[PcfTableType.PROPERTIES] = table

    @property
    def glyph_names(self) -> PcfGlyphNames | None:
        return self.tables.get(PcfTableType.GLYPH_NAMES, None)

    @glyph_names.setter
    def glyph_names(self, table: PcfGlyphNames | None):
        self.tables[PcfTableType.GLYPH_NAMES] = table

    def dump(self, stream: BinaryIO):
        buffer = Buffer(stream)

        headers = []
        table_offset = 8 + 16 * len(self.tables)
        for table in self.tables.values():
            table_format, table_size = table.dump(buffer, table_offset)
            headers.append(PcfHeader(table.table_type, table_format, table_size, table_offset))
            table_offset += table_size

        buffer.seek(0)
        buffer.write(_MAGIC_STRING)
        buffer.write_int_le(len(self.tables))
        for header in headers:
            header.dump(buffer)

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        with open(file_path, 'wb') as file:
            self.dump(file)
