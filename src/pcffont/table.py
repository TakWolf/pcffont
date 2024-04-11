from abc import abstractmethod

from pcffont.internal.buffer import Buffer


class PcfTable:
    DEFAULT_TABLE_FORMAT = 0b_1110
    DEFAULT_TABLE_FORMAT2 = 0b_0010

    def __init__(self, table_format: int):
        self.table_format = table_format

    @abstractmethod
    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        raise NotImplementedError

    def dump(self, buffer: Buffer, table_offset: int) -> int:
        table_size = self._dump(buffer, table_offset)

        # All tables begin on a 32bit boundary (and will be padded with zeroes).
        padding = 4 - table_size % 4
        if padding != 4:
            buffer.seek(table_offset + table_size)
            table_size += buffer.write_nulls(padding)

        return table_size
