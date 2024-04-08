from abc import abstractmethod

from pcffont.header import PcfTableType
from pcffont.internal.stream import Buffer


class PcfTable:
    @property
    @abstractmethod
    def table_type(self) -> PcfTableType:
        raise NotImplementedError

    @abstractmethod
    def dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        raise NotImplementedError
