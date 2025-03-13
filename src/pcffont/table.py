from abc import abstractmethod
from typing import Protocol, runtime_checkable

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.internal.stream import Stream


@runtime_checkable
class PcfTable(Protocol):
    table_format: PcfTableFormat

    @staticmethod
    @abstractmethod
    def parse(stream: Stream, font: 'pcffont.PcfFont', header: PcfHeader) -> 'PcfTable':
        raise NotImplementedError

    @abstractmethod
    def dump(self, stream: Stream, font: 'pcffont.PcfFont', table_offset: int) -> int:
        raise NotImplementedError
