from pcffont.error import PcfError
from pcffont.header import PcfTableType, PcfTableFormatMask, PcfHeader
from pcffont.internal.buffer import ByteOrder, Buffer
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


def parse_table(buffer: Buffer, header: PcfHeader) -> PcfTable | None:
    clz = TABLE_TYPE_REGISTRY.get(header.table_type, None)
    if clz is not None:
        return clz.parse(buffer, header)
    return None


def read_and_check_table_format(buffer: Buffer, header: PcfHeader) -> int:
    buffer.seek(header.table_offset)
    table_format = buffer.read_int32_le()
    if table_format != header.table_format:
        raise PcfError(f"The table format definition is inconsistent with the header: type '{header.table_type.name}', offset {header.table_offset}")
    return table_format


def get_table_byte_order(table_format: int) -> ByteOrder:
    byte_mask = table_format & PcfTableFormatMask.BYTE > 0
    bit_mask = table_format & PcfTableFormatMask.BIT > 0
    if byte_mask and bit_mask:
        return 'big'
    elif (not byte_mask) and (not bit_mask):
        return 'little'
    else:
        raise PcfError(f'Table format not supported: {table_format:b}')
