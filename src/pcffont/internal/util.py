from pcffont.error import PcfError
from pcffont.format import PcfTableFormatMask
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


def parse_table(buffer: Buffer, header: PcfHeader, strict_level: int = 1) -> PcfTable | None:
    clz = TABLE_TYPE_REGISTRY.get(header.table_type, None)
    if clz is not None:
        return clz.parse(buffer, header, strict_level)
    return None


def read_and_check_table_format(buffer: Buffer, header: PcfHeader) -> int:
    buffer.seek(header.table_offset)
    table_format = buffer.read_int32()
    if table_format != header.table_format:
        raise PcfError(f"The table format definition is inconsistent with the header: type '{header.table_type.name}', offset {header.table_offset}")
    return table_format


def is_ms_byte(table_format: int) -> bool:
    return table_format & PcfTableFormatMask.BYTE > 0


def is_ms_bit(table_format: int) -> bool:
    return table_format & PcfTableFormatMask.BIT > 0
