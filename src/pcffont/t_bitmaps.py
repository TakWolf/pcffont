from pcffont.header import PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.table import PcfTable


class PcfBitmaps(PcfTable):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfBitmaps':
        pass

    def __init__(self):
        pass

    def _dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        pass
