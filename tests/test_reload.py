import os
from pathlib import Path

from pcffont import PcfFont

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def test_reload(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.pcf')
    save_file_path = os.path.join(tmp_path, 'unifont-15.1.05.pcf')
    font = PcfFont.load(load_file_path)
    font.accelerators._compat_info = None
    font.bdf_accelerators._compat_info = None
    font.bitmaps._compat_info = None
    font.save(save_file_path)

    font_1 = PcfFont.load(load_file_path)
    font_2 = PcfFont.load(save_file_path)

    assert len(font_1) == len(font_2)
    for table_type, table_1 in font_1.items():
        table_2 = font_2[table_type]
        assert table_1.table_format.value == table_2.table_format.value

    assert len(font_1.properties) == len(font_2.properties)
    for key, value_1 in font_1.properties.items():
        value_2 = font_2.properties[key]
        assert value_1 == value_2

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

    assert font_1.accelerators.min_bounds.left_side_bearing == font_2.accelerators.min_bounds.left_side_bearing
    assert font_1.accelerators.min_bounds.right_side_bearing == font_2.accelerators.min_bounds.right_side_bearing
    assert font_1.accelerators.min_bounds.character_width == font_2.accelerators.min_bounds.character_width
    assert font_1.accelerators.min_bounds.ascent == font_2.accelerators.min_bounds.ascent
    assert font_1.accelerators.min_bounds.descent == font_2.accelerators.min_bounds.descent
    assert font_1.accelerators.min_bounds.attributes == font_2.accelerators.min_bounds.attributes == 0

    assert font_1.accelerators.ink_min_bounds is None
    assert font_1.accelerators.ink_max_bounds is None
    assert font_2.accelerators.ink_min_bounds is None
    assert font_2.accelerators.ink_max_bounds is None

    assert font_1.accelerators._compat_info is not None
    assert font_2.accelerators._compat_info is None

    assert len(font_1.metrics) == len(font_2.metrics)
    for glyph_index, metric_1 in enumerate(font_1.metrics):
        metric_2 = font_2.metrics[glyph_index]
        assert metric_1.left_side_bearing == metric_2.left_side_bearing
        assert metric_1.right_side_bearing == metric_2.right_side_bearing
        assert metric_1.character_width == metric_2.character_width
        assert metric_1.ascent == metric_2.ascent
        assert metric_1.descent == metric_2.descent
        assert metric_1.attributes == metric_2.attributes

    assert len(font_1.bitmaps) == len(font_2.bitmaps)
    for glyph_index, bitmap_1 in enumerate(font_1.bitmaps):
        bitmap_2 = font_2.bitmaps[glyph_index]
        assert len(bitmap_1) == len(bitmap_2)
        for i, bitmap_row_1 in enumerate(bitmap_1):
            bitmap_row_2 = bitmap_2[i]
            assert len(bitmap_row_1) == len(bitmap_row_2)
            bin_string_1 = ''.join(map(str, bitmap_row_1))
            bin_string_2 = ''.join(map(str, bitmap_row_2))
            assert bin_string_1 == bin_string_2

    assert font_1.ink_metrics is None
    assert font_2.ink_metrics is None

    assert len(font_1.bdf_encodings) == len(font_2.bdf_encodings)
    for code_point, glyph_index_1 in font_1.bdf_encodings.items():
        glyph_index_2 = font_2.bdf_encodings[code_point]
        assert glyph_index_1 == glyph_index_2
    assert font_1.bdf_encodings.default_char == font_2.bdf_encodings.default_char

    assert len(font_1.scalable_widths) == len(font_2.scalable_widths)
    for glyph_index, scalable_width_1 in enumerate(font_1.scalable_widths):
        scalable_width_2 = font_2.scalable_widths[glyph_index]
        assert scalable_width_1 == scalable_width_2

    assert len(font_1.glyph_names) == len(font_2.glyph_names)
    for glyph_index, glyph_name_1 in enumerate(font_1.glyph_names):
        glyph_name_2 = font_2.glyph_names[glyph_index]
        assert glyph_name_1 == glyph_name_2

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

    assert font_1.bdf_accelerators.min_bounds.left_side_bearing == font_2.bdf_accelerators.min_bounds.left_side_bearing
    assert font_1.bdf_accelerators.min_bounds.right_side_bearing == font_2.bdf_accelerators.min_bounds.right_side_bearing
    assert font_1.bdf_accelerators.min_bounds.character_width == font_2.bdf_accelerators.min_bounds.character_width
    assert font_1.bdf_accelerators.min_bounds.ascent == font_2.bdf_accelerators.min_bounds.ascent
    assert font_1.bdf_accelerators.min_bounds.descent == font_2.bdf_accelerators.min_bounds.descent
    assert font_1.bdf_accelerators.min_bounds.attributes == font_2.bdf_accelerators.min_bounds.attributes == 0

    assert font_1.bdf_accelerators.ink_min_bounds is None
    assert font_1.bdf_accelerators.ink_max_bounds is None
    assert font_2.bdf_accelerators.ink_min_bounds is None
    assert font_2.bdf_accelerators.ink_max_bounds is None

    assert font_1.bdf_accelerators._compat_info is not None
    assert font_2.bdf_accelerators._compat_info is None
