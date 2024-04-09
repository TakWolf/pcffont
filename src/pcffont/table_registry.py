from pcffont.glyph_names import PcfGlyphNames
from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.properties import PcfProperties
from pcffont.table import PcfTable

_table_registry = {
    PcfTableType.PROPERTIES: PcfProperties,
    PcfTableType.GLYPH_NAMES: PcfGlyphNames,
}


def parse(buffer: Buffer, header: PcfHeader) -> PcfTable | None:
    clz = _table_registry.get(header.table_type, None)
    if clz is not None:
        return clz.parse(buffer, header)
    return None
