from pcffont import PcfTableFormat, PcfMetric, PcfMetrics


def test_table_format_value():
    assert PcfTableFormat().value == 12
    assert PcfTableFormat(glyph_pad_index=2).value == 14
    assert PcfTableFormat(glyph_pad_index=2, ink_or_compressed_metrics=True).value == 270
    assert PcfTableFormat(ms_byte_first=False, ms_bit_first=False).value == 0
    assert PcfTableFormat(ms_byte_first=False, ms_bit_first=False, glyph_pad_index=2).value == 2
    assert PcfTableFormat(ms_byte_first=False, ms_bit_first=False, glyph_pad_index=2, ink_or_compressed_metrics=True).value == 258


def test_table_format_eq():
    table_format_1 = PcfTableFormat(ms_byte_first=False)
    table_format_2 = PcfTableFormat(ms_byte_first=False)
    table_format_3 = PcfTableFormat(glyph_pad_index=2)
    assert table_format_1 == table_format_2
    assert table_format_1 != table_format_3
    assert table_format_1 != 1
    assert table_format_1 != 'Hello World!'


def test_metric_eq():
    metric_1 = PcfMetric(
        left_side_bearing=-3,
        right_side_bearing=8,
        character_width=4,
        ascent=9,
        descent=-5,
    )
    metric_2 = PcfMetric(
        left_side_bearing=-3,
        right_side_bearing=8,
        character_width=4,
        ascent=9,
        descent=-5,
    )
    metric_3 = PcfMetric(
        left_side_bearing=-2,
        right_side_bearing=8,
        character_width=4,
        ascent=9,
        descent=-5,
    )
    assert metric_1 == metric_2
    assert metric_1 != metric_3
    assert metric_1 != 1
    assert metric_1 != 'Hello World!'


def test_metric_compressible():
    metric = PcfMetric(
        left_side_bearing=0,
        right_side_bearing=0,
        character_width=0,
        ascent=0,
        descent=-0,
    )
    assert metric.compressible

    metric.left_side_bearing = -129
    assert not metric.compressible
    metric.left_side_bearing = -128
    assert metric.compressible
    metric.left_side_bearing = 128
    assert not metric.compressible
    metric.left_side_bearing = 127
    assert metric.compressible

    metric.right_side_bearing = -129
    assert not metric.compressible
    metric.right_side_bearing = -128
    assert metric.compressible
    metric.right_side_bearing = 128
    assert not metric.compressible
    metric.right_side_bearing = 127
    assert metric.compressible

    metric.character_width = -129
    assert not metric.compressible
    metric.character_width = -128
    assert metric.compressible
    metric.character_width = 128
    assert not metric.compressible
    metric.character_width = 127
    assert metric.compressible

    metric.ascent = -129
    assert not metric.compressible
    metric.ascent = -128
    assert metric.compressible
    metric.ascent = 128
    assert not metric.compressible
    metric.ascent = 127
    assert metric.compressible

    metric.descent = -129
    assert not metric.compressible
    metric.descent = -128
    assert metric.compressible
    metric.descent = 128
    assert not metric.compressible
    metric.descent = 127
    assert metric.compressible


def test_metrics_calculate():
    metrics = PcfMetrics(metrics=[
        PcfMetric(
            left_side_bearing=-3,
            right_side_bearing=8,
            character_width=4,
            ascent=9,
            descent=-5,
        ),
        PcfMetric(
            left_side_bearing=7,
            right_side_bearing=3,
            character_width=1,
            ascent=-6,
            descent=0,
        ),
        PcfMetric(
            left_side_bearing=1,
            right_side_bearing=0,
            character_width=2,
            ascent=5,
            descent=4,
        ),
        PcfMetric(
            left_side_bearing=-5,
            right_side_bearing=-1,
            character_width=7,
            ascent=-3,
            descent=-9,
        ),
    ])
    assert metrics.calculate_min_bounds() == PcfMetric(
        left_side_bearing=-5,
        right_side_bearing=-1,
        character_width=1,
        ascent=-6,
        descent=-9,
    )
    assert metrics.calculate_max_bounds() == PcfMetric(
        left_side_bearing=7,
        right_side_bearing=8,
        character_width=7,
        ascent=9,
        descent=4,
    )
    assert metrics.calculate_max_overlap() == 4
    assert metrics.calculate_compressible()
    metrics[0].left_side_bearing = 128
    assert not metrics.calculate_compressible()
