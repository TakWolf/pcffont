from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.t_encodings import PcfBdfEncodings
from pcffont.t_glyph_names import PcfGlyphNames
from pcffont.t_metrics import PcfMetrics
from pcffont.t_properties import PcfProperties
from pcffont.t_scalable_widths import PcfScalableWidths
from pcffont.table import PcfTable

TYPE_REGISTRY = {
    PcfTableType.PROPERTIES: PcfProperties,
    PcfTableType.ACCELERATORS: None,
    PcfTableType.METRICS: PcfMetrics,
    PcfTableType.BITMAPS: None,
    PcfTableType.INK_METRICS: PcfMetrics,
    PcfTableType.BDF_ENCODINGS: PcfBdfEncodings,
    PcfTableType.SWIDTHS: PcfScalableWidths,
    PcfTableType.GLYPH_NAMES: PcfGlyphNames,
    PcfTableType.BDF_ACCELERATORS: None,
}


def parse_table(buffer: Buffer, header: PcfHeader) -> PcfTable | None:
    clz = TYPE_REGISTRY.get(header.table_type, None)
    if clz is not None:
        return clz.parse(buffer, header)
    return None
