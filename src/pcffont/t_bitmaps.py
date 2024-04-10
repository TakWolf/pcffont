from pcffont.header import PcfTableFormat, PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


# TODO
class PcfBitmaps(PcfTable):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfBitmaps':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)

        # TODO
        obj = PcfBitmaps(table_format)
        buffer.seek(header.table_offset)
        obj.chunk = buffer.read(header.table_size)
        return obj

    def __init__(
            self,
            table_format: int = PcfTableFormat.BYTE_ORDER_BIG,
    ):
        PcfTable.__init__(self, table_format)

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        # TODO
        buffer.seek(table_offset)
        return buffer.write(self.chunk)
