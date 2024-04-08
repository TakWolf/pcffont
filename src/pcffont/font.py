import os
from typing import BinaryIO

from pcffont.error import PcfError
from pcffont.header import PcfTableType, PcfTableFormatMask, PcfHeader
from pcffont.internal.stream import ByteOrder, Buffer
from pcffont.properties import PcfProperties


class PcfFont:
    @staticmethod
    def parse(stream: BinaryIO) -> 'PcfFont':
        buffer = Buffer(stream)

        buffer.seek(0)
        headers = PcfHeader.parse(buffer)

        tables = {}
        for i, header in enumerate(headers):
            if header.table_type in tables:
                raise PcfError(f"Duplicate table '{header.table_type.name}'")

            buffer.seek(header.offset)
            table_format = buffer.read_int_le()
            if table_format != header.table_format:
                raise PcfError(f"The table format definition is inconsistent with the header: type '{header.table_type.name}', header index {i}, offset {header.offset}")

            byte_order: ByteOrder = 'little'
            if (table_format & (PcfTableFormatMask.BYTE | PcfTableFormatMask.BIT)) > 0:
                byte_order = 'big'

            if header.table_type == PcfTableType.PROPERTIES:
                properties = PcfProperties.parse(buffer, byte_order)
                tables[header.table_type] = properties

        return PcfFont(
            tables.get(PcfTableType.PROPERTIES, None),
        )

    @staticmethod
    def load(file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> 'PcfFont':
        with open(file_path, 'rb') as file:
            return PcfFont.parse(file)

    def __init__(
            self,
            properties: PcfProperties = None,
    ):
        self.properties = properties

    def dump(self, stream: BinaryIO):
        buffer = Buffer(stream)

        # TODO

        pass

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        with open(file_path, 'wb') as file:
            self.dump(file)
