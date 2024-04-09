from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.t_glyph_names import PcfGlyphNames
from pcffont.t_metrics import PcfMetrics
from pcffont.t_properties import PcfProperties
from pcffont.t_scalable_widths import PcfScalableWidths
from pcffont.table import PcfTable

_table_registry = {
    PcfTableType.PROPERTIES: PcfProperties,
    PcfTableType.ACCELERATORS: None,
    PcfTableType.METRICS: PcfMetrics,
    PcfTableType.BITMAPS: None,
    PcfTableType.INK_METRICS: None,
    PcfTableType.BDF_ENCODINGS: None,
    PcfTableType.SWIDTHS: PcfScalableWidths,
    PcfTableType.GLYPH_NAMES: PcfGlyphNames,
    PcfTableType.BDF_ACCELERATORS: None,
}


def parse(buffer: Buffer, header: PcfHeader) -> PcfTable | None:
    clz = _table_registry.get(header.table_type, None)
    if clz is not None:
        return clz.parse(buffer, header)
    return None
