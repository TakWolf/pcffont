from pcffont.header import PcfTableType, PcfTableFormat, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.table import PcfTable


class PcfMetrics(PcfTable):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfMetrics':
        table_format, byte_order = header.get_and_check_table_format(buffer)

        is_compressed = False
        if table_format & PcfTableFormat.COMPRESSED_METRICS > 0:
            is_compressed = True

        if is_compressed:
            pass
        else:
            pass

        # TODO
        buffer.seek(header.table_offset)
        data = buffer.read(header.table_size)

        metrics = PcfMetrics()
        metrics.header = header
        metrics.data = data
        return metrics
        # TODO

    def __init__(self):
        pass

    @property
    def table_type(self) -> PcfTableType:
        return PcfTableType.METRICS

    def dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        # TODO
        buffer.seek(table_offset)
        buffer.write(self.data)
        return self.header.table_format, self.header.table_size
