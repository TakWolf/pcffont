from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.buffer import Buffer
from pcffont.t_accelerators import PcfAccelerators
from pcffont.t_bitmaps import PcfBitmaps
from pcffont.t_encodings import PcfBdfEncodings
from pcffont.t_glyph_names import PcfGlyphNames
from pcffont.t_metrics import PcfMetrics
from pcffont.t_properties import PcfProperties
from pcffont.t_scalable_widths import PcfScalableWidths
from pcffont.table import PcfTable

TABLE_TYPE_REGISTRY = {
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


def parse_table(buffer: Buffer, header: PcfHeader, strict_level: int = 1) -> PcfTable:
    return TABLE_TYPE_REGISTRY[header.table_type].parse(buffer, header, strict_level)
