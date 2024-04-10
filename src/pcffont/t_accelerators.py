from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer
from pcffont.table import PcfTable


# TODO
class PcfAccelerators(PcfTable):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfAccelerators':
        table_format = util.read_and_check_table_format(buffer, header)
        byte_order = util.get_table_byte_order(table_format)

        # TODO
        obj = PcfAccelerators(table_format)
        buffer.seek(header.table_offset)
        obj.chuck = buffer.read(header.table_size)
        obj.table_size = header.table_size
        return obj

    def __init__(
            self,
            table_format: int = 0b1110,
    ):
        PcfTable.__init__(self, table_format)

    def _dump(self, buffer: Buffer, table_offset: int) -> int:
        # TODO
        buffer.seek(table_offset)
        buffer.write(self.chuck)
        return self.table_size
