from abc import abstractmethod

from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer


class PcfTable:
    @property
    @abstractmethod
    def table_type(self) -> PcfTableType:
        raise NotImplementedError

    @abstractmethod
    def _dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        raise NotImplementedError

    def dump(self, buffer: Buffer, table_offset: int) -> PcfHeader:
        table_format, table_size = self._dump(buffer, table_offset)

        padding = 4 - table_size % 4
        if padding != 4:
            buffer.seek(table_offset + table_size)
            buffer.write_nulls(padding)
            table_size += padding

        return PcfHeader(self.table_type, table_format, table_size, table_offset)
