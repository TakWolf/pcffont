from pcffont import PcfTableFormat


def test_value():
    assert PcfTableFormat().value == 0
    assert PcfTableFormat(glyph_pad_index=2).value == 2
    assert PcfTableFormat(ms_byte_first=True, ms_bit_first=True).value == 12
    assert PcfTableFormat(ms_byte_first=True, ms_bit_first=True, glyph_pad_index=2).value == 14
    assert PcfTableFormat(ink_bounds_or_compressed_metrics=True, glyph_pad_index=2).value == 258
    assert PcfTableFormat(ms_byte_first=True, ms_bit_first=True, ink_bounds_or_compressed_metrics=True, glyph_pad_index=2).value == 270


def test_parse():
    table_format = PcfTableFormat.parse(270)
    assert table_format.ms_byte_first == True
    assert table_format.ms_bit_first == True
    assert table_format.ink_bounds_or_compressed_metrics == True
    assert table_format.glyph_pad_index == 2
    assert table_format.scan_unit_index == 0


def test_eq():
    table_format_1 = PcfTableFormat(ms_byte_first=True)
    table_format_2 = PcfTableFormat(ms_byte_first=True)
    table_format_3 = PcfTableFormat(glyph_pad_index=2)
    assert table_format_1 == table_format_2
    assert table_format_1 != table_format_3
    assert table_format_1 != 1
    assert table_format_1 != 'Hello World!'
