from pcffont import PcfMetrics, PcfMetric


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
