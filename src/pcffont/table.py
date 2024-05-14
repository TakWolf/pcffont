from abc import abstractmethod
from typing import Protocol, runtime_checkable

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.buffer import Buffer


@runtime_checkable
class PcfTable(Protocol):
    table_format: PcfTableFormat

    @staticmethod
    @abstractmethod
    def parse(buffer: Buffer, font: 'pcffont.PcfFont', header: PcfHeader, strict_level: int) -> 'PcfTable':
        raise NotImplementedError

    @abstractmethod
    def dump(self, buffer: Buffer, font: 'pcffont.PcfFont', table_offset: int) -> int:
        raise NotImplementedError
