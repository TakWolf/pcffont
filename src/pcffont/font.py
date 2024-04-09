import os
from collections import UserDict
from typing import BinaryIO

from pcffont import table_registry
from pcffont.error import PcfError
from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.t_accelerators import PcfAccelerators
from pcffont.t_bitmaps import PcfBitmaps
from pcffont.t_encodings import PcfBdfEncodings
from pcffont.t_glyph_names import PcfGlyphNames
from pcffont.t_metrics import PcfMetrics
from pcffont.t_properties import PcfProperties
from pcffont.t_scalable_widths import PcfScalableWidths
from pcffont.table import PcfTable

_MAGIC_STRING = b'\x01fcp'


class PcfFont(UserDict[PcfTableType, PcfTable]):
    @staticmethod
    def parse(stream: BinaryIO) -> 'PcfFont':
        buffer = Buffer(stream)

        buffer.seek(0)
        if buffer.read(4) != _MAGIC_STRING:
            raise PcfError('Not PCF format')

        headers = PcfHeader.parse(buffer)
        tables = {table_type: table_registry.parse_table(buffer, header) for table_type, header in headers.items()}

        return PcfFont(tables)

    @staticmethod
    def load(file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> 'PcfFont':
        with open(file_path, 'rb') as file:
            return PcfFont.parse(file)

    def __init__(self, tables: dict[PcfTableType, PcfTable | None] = None):
        super().__init__(tables)

    def __setitem__(self, table_type: PcfTableType, table: PcfTable | None):
        if table is None:
            self.pop(table_type, None)
        else:
            assert isinstance(table, table_registry.TYPE_REGISTRY[table_type])
            super().__setitem__(table_type, table)

    @property
    def properties(self) -> PcfProperties | None:
        return self.get(PcfTableType.PROPERTIES, None)

    @properties.setter
    def properties(self, table: PcfProperties | None):
        self[PcfTableType.PROPERTIES] = table

    @property
    def accelerators(self) -> PcfAccelerators | None:
        return self.get(PcfTableType.ACCELERATORS, None)

    @accelerators.setter
    def accelerators(self, table: PcfAccelerators | None):
        self[PcfTableType.ACCELERATORS] = table

    @property
    def metrics(self) -> PcfMetrics | None:
        return self.get(PcfTableType.METRICS, None)

    @metrics.setter
    def metrics(self, table: PcfMetrics | None):
        self[PcfTableType.METRICS] = table

    @property
    def bitmaps(self) -> PcfBitmaps | None:
        return self.get(PcfTableType.BITMAPS, None)

    @bitmaps.setter
    def bitmaps(self, table: PcfBitmaps | None):
        self[PcfTableType.BITMAPS] = table

    @property
    def ink_metrics(self) -> PcfMetrics | None:
        return self.get(PcfTableType.INK_METRICS, None)

    @ink_metrics.setter
    def ink_metrics(self, table: PcfMetrics | None):
        self[PcfTableType.INK_METRICS] = table

    @property
    def bdf_encodings(self) -> PcfBdfEncodings | None:
        return self.get(PcfTableType.BDF_ENCODINGS, None)

    @bdf_encodings.setter
    def bdf_encodings(self, table: PcfBdfEncodings | None):
        self[PcfTableType.BDF_ENCODINGS] = table

    @property
    def scalable_widths(self) -> PcfScalableWidths | None:
        return self.get(PcfTableType.SWIDTHS, None)

    @scalable_widths.setter
    def scalable_widths(self, table: PcfScalableWidths | None):
        self[PcfTableType.SWIDTHS] = table

    @property
    def glyph_names(self) -> PcfGlyphNames | None:
        return self.get(PcfTableType.GLYPH_NAMES, None)

    @glyph_names.setter
    def glyph_names(self, table: PcfGlyphNames | None):
        self[PcfTableType.GLYPH_NAMES] = table

    @property
    def bdf_accelerators(self) -> PcfAccelerators | None:
        return self.get(PcfTableType.BDF_ACCELERATORS, None)

    @bdf_accelerators.setter
    def bdf_accelerators(self, table: PcfAccelerators | None):
        self[PcfTableType.BDF_ACCELERATORS] = table

    def dump(self, stream: BinaryIO):
        buffer = Buffer(stream)

        headers = []
        table_offset = 8 + 16 * len(self)
        for table_type, table in self:
            header = table.dump(buffer, table_type, table_offset)
            headers.append(header)
            table_offset += header.table_size

        buffer.seek(0)
        buffer.write(_MAGIC_STRING)
        buffer.write_int32_le(len(self))
        for header in headers:
            header.dump(buffer)

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        with open(file_path, 'wb') as file:
            self.dump(file)
