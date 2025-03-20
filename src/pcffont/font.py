from collections import UserDict
from io import BytesIO
from os import PathLike
from typing import Any, BinaryIO

from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Stream
from pcffont.t_accelerators import PcfAccelerators
from pcffont.t_bitmaps import PcfBitmaps
from pcffont.t_encodings import PcfBdfEncodings
from pcffont.t_glyph_names import PcfGlyphNames
from pcffont.t_metrics import PcfMetrics
from pcffont.t_properties import PcfProperties
from pcffont.t_scalable_widths import PcfScalableWidths
from pcffont.table import PcfTable

_TABLE_TYPE_REGISTRY = {
    PcfTableType.PROPERTIES: PcfProperties,
    PcfTableType.ACCELERATORS: PcfAccelerators,
    PcfTableType.METRICS: PcfMetrics,
    PcfTableType.BITMAPS: PcfBitmaps,
    PcfTableType.INK_METRICS: PcfMetrics,
    PcfTableType.BDF_ENCODINGS: PcfBdfEncodings,
    PcfTableType.SWIDTHS: PcfScalableWidths,
    PcfTableType.GLYPH_NAMES: PcfGlyphNames,
    PcfTableType.BDF_ACCELERATORS: PcfAccelerators,
}


class PcfFont(UserDict[PcfTableType, PcfTable]):
    @staticmethod
    def parse(stream: bytes | BinaryIO) -> 'PcfFont':
        if isinstance(stream, bytes):
            stream = BytesIO(stream)
        stream = Stream(stream)

        font = PcfFont()
        headers = PcfHeader.parse(stream)
        for header in headers:
            table = _TABLE_TYPE_REGISTRY[header.table_type].parse(stream, font, header)
            font[header.table_type] = table
        return font

    @staticmethod
    def load(file_path: str | PathLike[str]) -> 'PcfFont':
        with open(file_path, 'rb') as file:
            return PcfFont.parse(file)

    def __setitem__(self, table_type: Any, table: Any):
        if not isinstance(table_type, PcfTableType):
            raise KeyError(f"expected type 'PcfTableType', got '{type(table_type).__name__}' instead")

        if table is None:
            self.pop(table_type, None)
            return

        if not isinstance(table, _TABLE_TYPE_REGISTRY[table_type]):
            raise ValueError(f"illegal value type: '{type(table).__name__}'")

        super().__setitem__(table_type, table)

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfFont):
            return False
        return super().__eq__(other)

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
        stream = Stream(stream)

        headers = []
        table_offset = 4 + 4 + (4 * 4) * len(self)
        for table_type, table in sorted(self.items()):
            table_size = table.dump(stream, self, table_offset)
            headers.append(PcfHeader(table_type, table.table_format, table_size, table_offset))
            table_offset += table_size

        PcfHeader.dump(stream, headers)

    def dump_to_bytes(self) -> bytes:
        stream = BytesIO()
        self.dump(stream)
        return stream.getvalue()

    def save(self, file_path: str | PathLike[str]):
        with open(file_path, 'wb') as file:
            self.dump(file)
