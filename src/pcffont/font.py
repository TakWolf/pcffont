import os
from typing import BinaryIO

from pcffont.error import PcfError
from pcffont.header import PcfTableType, PcfTableFormatMask, PcfHeader
from pcffont.internal.stream import ByteOrder, Buffer
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

        tables = {}
        headers = PcfHeader.parse(buffer)
        for i, header in enumerate(headers):
            if header.table_type in tables:
                raise PcfError(f"Duplicate table '{header.table_type.name}'")

            buffer.seek(header.table_offset)
            table_format = buffer.read_int_le()
            if table_format != header.table_format:
                raise PcfError(f"The table format definition is inconsistent with the header: type '{header.table_type.name}', index {i}, offset {header.table_offset}")

            byte_order: ByteOrder = 'little'
            if (table_format & (PcfTableFormatMask.BYTE | PcfTableFormatMask.BIT)) > 0:
                byte_order = 'big'

            if header.table_type == PcfTableType.PROPERTIES:
                tables[header.table_type] = PcfProperties.parse(buffer, byte_order)
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
