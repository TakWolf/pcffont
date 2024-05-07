import os

from bdffont import BdfFont

from pcffont import PcfFont, PcfFontBuilder, PcfGlyph

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _load_by_bdf(file_path: str) -> PcfFont:
    bdf_font = BdfFont.load(file_path)

    builder = PcfFontBuilder()
    builder.configs.font_ascent = bdf_font.properties.font_ascent
    builder.configs.font_descent = bdf_font.properties.font_descent
    builder.configs.glyph_pad_index = 2

    for bdf_glyph in bdf_font.glyphs:
        builder.glyphs.append(PcfGlyph(
            name=bdf_glyph.name,
            encoding=bdf_glyph.encoding,
            scalable_width=bdf_glyph.scalable_width_x,
            character_width=bdf_glyph.device_width_x,
            dimensions=bdf_glyph.dimensions,
            origin=bdf_glyph.origin,
            bitmap=bdf_glyph.bitmap,
        ))

    builder.properties.update(bdf_font.properties)

    return builder.build()


def test_unifont():
    font_1 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.pcf'))
    font_2 = _load_by_bdf(os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.bdf'))

    assert font_1.metrics.table_format == font_2.metrics.table_format
    for glyph_index, metric_1 in enumerate(font_1.metrics):
        metric_2 = font_2.metrics[glyph_index]
        assert metric_1 == metric_2

    assert font_1.ink_metrics is None
    assert font_2.ink_metrics is None

    assert font_1.accelerators.table_format == font_2.accelerators.table_format
    assert font_1.accelerators.no_overlap == font_2.accelerators.no_overlap
    assert font_1.accelerators.constant_metrics == font_2.accelerators.constant_metrics
    assert font_1.accelerators.terminal_font == font_2.accelerators.terminal_font
    assert font_1.accelerators.constant_width == font_2.accelerators.constant_width
    assert font_1.accelerators.ink_inside == font_2.accelerators.ink_inside
    assert font_1.accelerators.ink_metrics == font_2.accelerators.ink_metrics
    assert font_1.accelerators.draw_right_to_left == font_2.accelerators.draw_right_to_left
    assert font_1.accelerators.font_ascent == font_2.accelerators.font_ascent
    assert font_1.accelerators.font_descent == font_2.accelerators.font_descent
    assert font_1.accelerators.max_overlap == font_2.accelerators.max_overlap
    assert font_1.accelerators.min_bounds == font_2.accelerators.min_bounds
    assert font_1.accelerators.max_bounds == font_2.accelerators.max_bounds
    assert font_1.accelerators.ink_min_bounds is None
    assert font_1.accelerators.ink_max_bounds is None
    assert font_2.accelerators.ink_min_bounds is None
    assert font_2.accelerators.ink_max_bounds is None

    assert font_1.bdf_accelerators.table_format == font_2.bdf_accelerators.table_format
    assert font_1.bdf_accelerators.no_overlap == font_2.bdf_accelerators.no_overlap
    assert font_1.bdf_accelerators.constant_metrics == font_2.bdf_accelerators.constant_metrics
    assert font_1.bdf_accelerators.terminal_font == font_2.bdf_accelerators.terminal_font
    assert font_1.bdf_accelerators.constant_width == font_2.bdf_accelerators.constant_width
    assert font_1.bdf_accelerators.ink_inside == font_2.bdf_accelerators.ink_inside
    assert font_1.bdf_accelerators.ink_metrics == font_2.bdf_accelerators.ink_metrics
    assert font_1.bdf_accelerators.draw_right_to_left == font_2.bdf_accelerators.draw_right_to_left
    assert font_1.bdf_accelerators.font_ascent == font_2.bdf_accelerators.font_ascent
    assert font_1.bdf_accelerators.font_descent == font_2.bdf_accelerators.font_descent
    assert font_1.bdf_accelerators.max_overlap == font_2.bdf_accelerators.max_overlap
    assert font_1.bdf_accelerators.min_bounds == font_2.bdf_accelerators.min_bounds
    assert font_1.bdf_accelerators.max_bounds == font_2.bdf_accelerators.max_bounds
    assert font_1.bdf_accelerators.ink_min_bounds is None
    assert font_1.bdf_accelerators.ink_max_bounds is None
    assert font_2.bdf_accelerators.ink_min_bounds is None
    assert font_2.bdf_accelerators.ink_max_bounds is None


def test_demo():
    font_1 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo.pcf'))
    font_2 = _load_by_bdf(os.path.join(project_root_dir, 'assets', 'demo', 'demo.bdf'))

    assert font_1.metrics.table_format == font_2.metrics.table_format
    for glyph_index, metric_1 in enumerate(font_1.metrics):
        metric_2 = font_2.metrics[glyph_index]
        assert metric_1 == metric_2

    assert font_1.ink_metrics.table_format == font_2.ink_metrics.table_format
    for glyph_index, ink_metric_1 in enumerate(font_1.ink_metrics):
        ink_metric_2 = font_2.ink_metrics[glyph_index]
        assert ink_metric_1 == ink_metric_2

    assert font_1.accelerators.table_format == font_2.accelerators.table_format
    assert font_1.accelerators.no_overlap == font_2.accelerators.no_overlap
    assert font_1.accelerators.constant_metrics == font_2.accelerators.constant_metrics
    assert font_1.accelerators.terminal_font == font_2.accelerators.terminal_font
    assert font_1.accelerators.constant_width == font_2.accelerators.constant_width
    assert font_1.accelerators.ink_inside == font_2.accelerators.ink_inside
    assert font_1.accelerators.ink_metrics == font_2.accelerators.ink_metrics
    assert font_1.accelerators.draw_right_to_left == font_2.accelerators.draw_right_to_left
    assert font_1.accelerators.font_ascent == font_2.accelerators.font_ascent
    assert font_1.accelerators.font_descent == font_2.accelerators.font_descent
    assert font_1.accelerators.max_overlap == font_2.accelerators.max_overlap
    assert font_1.accelerators.min_bounds == font_2.accelerators.min_bounds
    assert font_1.accelerators.max_bounds == font_2.accelerators.max_bounds
    assert font_1.accelerators.ink_min_bounds == font_2.accelerators.ink_min_bounds
    assert font_1.accelerators.ink_max_bounds == font_2.accelerators.ink_max_bounds

    assert font_1.bdf_accelerators.table_format == font_2.bdf_accelerators.table_format
    assert font_1.bdf_accelerators.no_overlap == font_2.bdf_accelerators.no_overlap
    assert font_1.bdf_accelerators.constant_metrics == font_2.bdf_accelerators.constant_metrics
    assert font_1.bdf_accelerators.terminal_font == font_2.bdf_accelerators.terminal_font
    assert font_1.bdf_accelerators.constant_width == font_2.bdf_accelerators.constant_width
    assert font_1.bdf_accelerators.ink_inside == font_2.bdf_accelerators.ink_inside
    assert font_1.bdf_accelerators.ink_metrics == font_2.bdf_accelerators.ink_metrics
    assert font_1.bdf_accelerators.draw_right_to_left == font_2.bdf_accelerators.draw_right_to_left
    assert font_1.bdf_accelerators.font_ascent == font_2.bdf_accelerators.font_ascent
    assert font_1.bdf_accelerators.font_descent == font_2.bdf_accelerators.font_descent
    assert font_1.bdf_accelerators.max_overlap == font_2.bdf_accelerators.max_overlap
    assert font_1.bdf_accelerators.min_bounds == font_2.bdf_accelerators.min_bounds
    assert font_1.bdf_accelerators.max_bounds == font_2.bdf_accelerators.max_bounds
    assert font_1.bdf_accelerators.ink_min_bounds == font_2.bdf_accelerators.ink_min_bounds
    assert font_1.bdf_accelerators.ink_max_bounds == font_2.bdf_accelerators.ink_max_bounds


def test_demo_2():
    font_1 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-2.pcf'))
    font_2 = _load_by_bdf(os.path.join(project_root_dir, 'assets', 'demo', 'demo-2.bdf'))

    assert font_1.metrics.table_format == font_2.metrics.table_format
    for glyph_index, metric_1 in enumerate(font_1.metrics):
        metric_2 = font_2.metrics[glyph_index]
        assert metric_1 == metric_2

    assert font_1.ink_metrics.table_format == font_2.ink_metrics.table_format
    for glyph_index, ink_metric_1 in enumerate(font_1.ink_metrics):
        ink_metric_2 = font_2.ink_metrics[glyph_index]
        assert ink_metric_1 == ink_metric_2

    assert font_1.accelerators.table_format == font_2.accelerators.table_format
    assert font_1.accelerators.no_overlap == font_2.accelerators.no_overlap
    assert font_1.accelerators.constant_metrics == font_2.accelerators.constant_metrics
    assert font_1.accelerators.terminal_font == font_2.accelerators.terminal_font
    assert font_1.accelerators.constant_width == font_2.accelerators.constant_width
    assert font_1.accelerators.ink_inside == font_2.accelerators.ink_inside
    assert font_1.accelerators.ink_metrics == font_2.accelerators.ink_metrics
    assert font_1.accelerators.draw_right_to_left == font_2.accelerators.draw_right_to_left
    assert font_1.accelerators.font_ascent == font_2.accelerators.font_ascent
    assert font_1.accelerators.font_descent == font_2.accelerators.font_descent
    assert font_1.accelerators.max_overlap == font_2.accelerators.max_overlap
    assert font_1.accelerators.min_bounds == font_2.accelerators.min_bounds
    assert font_1.accelerators.max_bounds == font_2.accelerators.max_bounds
    assert font_1.accelerators.ink_min_bounds == font_2.accelerators.ink_min_bounds
    assert font_1.accelerators.ink_max_bounds == font_2.accelerators.ink_max_bounds

    assert font_1.bdf_accelerators.table_format == font_2.bdf_accelerators.table_format
    assert font_1.bdf_accelerators.no_overlap == font_2.bdf_accelerators.no_overlap
    assert font_1.bdf_accelerators.constant_metrics == font_2.bdf_accelerators.constant_metrics
    assert font_1.bdf_accelerators.terminal_font == font_2.bdf_accelerators.terminal_font
    assert font_1.bdf_accelerators.constant_width == font_2.bdf_accelerators.constant_width
    assert font_1.bdf_accelerators.ink_inside == font_2.bdf_accelerators.ink_inside
    assert font_1.bdf_accelerators.ink_metrics == font_2.bdf_accelerators.ink_metrics
    assert font_1.bdf_accelerators.draw_right_to_left == font_2.bdf_accelerators.draw_right_to_left
    assert font_1.bdf_accelerators.font_ascent == font_2.bdf_accelerators.font_ascent
    assert font_1.bdf_accelerators.font_descent == font_2.bdf_accelerators.font_descent
    assert font_1.bdf_accelerators.max_overlap == font_2.bdf_accelerators.max_overlap
    assert font_1.bdf_accelerators.min_bounds == font_2.bdf_accelerators.min_bounds
    assert font_1.bdf_accelerators.max_bounds == font_2.bdf_accelerators.max_bounds
    assert font_1.bdf_accelerators.ink_min_bounds == font_2.bdf_accelerators.ink_min_bounds
    assert font_1.bdf_accelerators.ink_max_bounds == font_2.bdf_accelerators.ink_max_bounds
