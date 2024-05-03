from abc import abstractmethod

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.internal.buffer import Buffer


class PcfTable:
    def __init__(self, table_format: PcfTableFormat):
        self.table_format = table_format

    def __repr__(self) -> str:
        return object.__repr__(self)

    @abstractmethod
    def _dump(self, buffer: Buffer, font: 'pcffont.PcfFont', table_offset: int) -> int:
        raise NotImplementedError

    def dump(self, buffer: Buffer, font: 'pcffont.PcfFont', table_offset: int) -> int:
        table_size = self._dump(buffer, font, table_offset)

        # All tables begin on a 32bit boundary (and will be padded with zeroes).
        padding = 4 - table_size % 4
        if padding != 4:
            buffer.seek(table_offset + table_size)
            table_size += buffer.write_nulls(padding)

        return table_size
