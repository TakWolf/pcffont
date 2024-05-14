from abc import abstractmethod

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.internal.buffer import Buffer


class PcfTable:
    def __init__(self, table_format: PcfTableFormat):
        self.table_format = table_format

    @abstractmethod
    def dump(self, buffer: Buffer, font: 'pcffont.PcfFont', table_offset: int) -> int:
        raise NotImplementedError
