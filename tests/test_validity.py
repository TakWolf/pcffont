import os

from pcffont import PcfFont

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def test_demo():
    font_1 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-lsbyte-lsbit-p4-u2.pcf'))
    font_2 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-lsbyte-msbit-p4-u2.pcf'))
    font_3 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-msbyte-lsbit-p4-u2.pcf'))
    font_4 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-msbyte-msbit-p4-u2.pcf'))
    font_5 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-lsbyte-lsbit-p2-u4.pcf'))
    font_6 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-lsbyte-msbit-p2-u4.pcf'))
    font_7 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-msbyte-lsbit-p2-u4.pcf'))
    font_8 = PcfFont.load(os.path.join(project_root_dir, 'assets', 'demo', 'demo-msbyte-msbit-p2-u4.pcf'))

    assert len(font_1.metrics) == len(font_2.metrics) == len(font_3.metrics) == len(font_4.metrics) == len(font_5.metrics) == len(font_6.metrics) == len(font_7.metrics) == len(font_8.metrics)
    for glyph_index, metric_1 in enumerate(font_1.metrics):
        metric_2 = font_2.metrics[glyph_index]
        metric_3 = font_3.metrics[glyph_index]
        metric_4 = font_4.metrics[glyph_index]
        metric_5 = font_5.metrics[glyph_index]
        metric_6 = font_6.metrics[glyph_index]
        metric_7 = font_7.metrics[glyph_index]
        metric_8 = font_8.metrics[glyph_index]
        assert metric_1.left_side_bearing == metric_2.left_side_bearing == metric_3.left_side_bearing == metric_4.left_side_bearing == metric_5.left_side_bearing == metric_6.left_side_bearing == metric_7.left_side_bearing == metric_8.left_side_bearing
        assert metric_1.right_side_bearing == metric_2.right_side_bearing == metric_3.right_side_bearing == metric_4.right_side_bearing == metric_5.right_side_bearing == metric_6.right_side_bearing == metric_7.right_side_bearing == metric_8.right_side_bearing
        assert metric_1.character_width == metric_2.character_width == metric_3.character_width == metric_4.character_width == metric_5.character_width == metric_6.character_width == metric_7.character_width == metric_8.character_width
        assert metric_1.ascent == metric_2.ascent == metric_3.ascent == metric_4.ascent == metric_5.ascent == metric_6.ascent == metric_7.ascent == metric_8.ascent
        assert metric_1.descent == metric_2.descent == metric_3.descent == metric_4.descent == metric_5.descent == metric_6.descent == metric_7.descent == metric_8.descent
        assert metric_1.attributes == metric_2.attributes == metric_3.attributes == metric_4.attributes == metric_5.attributes == metric_6.attributes == metric_7.attributes == metric_8.attributes

    assert len(font_1.bitmaps) == len(font_2.bitmaps) == len(font_3.bitmaps) == len(font_4.bitmaps) == len(font_5.bitmaps) == len(font_6.bitmaps) == len(font_7.bitmaps) == len(font_8.bitmaps)
    for glyph_index, bitmap_1 in enumerate(font_1.bitmaps):
        bitmap_2 = font_2.bitmaps[glyph_index]
        bitmap_3 = font_3.bitmaps[glyph_index]
        bitmap_4 = font_4.bitmaps[glyph_index]
        bitmap_5 = font_5.bitmaps[glyph_index]
        bitmap_6 = font_6.bitmaps[glyph_index]
        bitmap_7 = font_7.bitmaps[glyph_index]
        bitmap_8 = font_8.bitmaps[glyph_index]
        assert len(bitmap_1) == len(bitmap_2) == len(bitmap_3) == len(bitmap_4) == len(bitmap_5) == len(bitmap_6) == len(bitmap_7) == len(bitmap_8)
        for i, bitmap_row_1 in enumerate(bitmap_1):
            bitmap_row_2 = bitmap_2[i]
            bitmap_row_3 = bitmap_3[i]
            bitmap_row_4 = bitmap_4[i]
            bitmap_row_5 = bitmap_5[i]
            bitmap_row_6 = bitmap_6[i]
            bitmap_row_7 = bitmap_7[i]
            bitmap_row_8 = bitmap_8[i]
            assert len(bitmap_row_1) == len(bitmap_row_2) == len(bitmap_row_3) == len(bitmap_row_4) == len(bitmap_row_5) == len(bitmap_row_6) == len(bitmap_row_7) == len(bitmap_row_8)
            bin_string_1 = ''.join(map(str, bitmap_row_1))
            bin_string_2 = ''.join(map(str, bitmap_row_2))
            bin_string_3 = ''.join(map(str, bitmap_row_3))
            bin_string_4 = ''.join(map(str, bitmap_row_4))
            bin_string_5 = ''.join(map(str, bitmap_row_5))
            bin_string_6 = ''.join(map(str, bitmap_row_6))
            bin_string_7 = ''.join(map(str, bitmap_row_7))
            bin_string_8 = ''.join(map(str, bitmap_row_8))
            assert bin_string_1 == bin_string_2 == bin_string_3 == bin_string_4 == bin_string_5 == bin_string_6 == bin_string_7 == bin_string_8
