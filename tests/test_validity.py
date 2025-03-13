from pathlib import Path

from bdffont import BdfFont

from pcffont import PcfFont


def test_demo(assets_dir: Path):
    font_0 = BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))
    font_1 = PcfFont.load(assets_dir.joinpath('demo', 'demo-lsbyte-lsbit-p4-u2.pcf'))
    font_2 = PcfFont.load(assets_dir.joinpath('demo', 'demo-lsbyte-msbit-p4-u2.pcf'))
    font_3 = PcfFont.load(assets_dir.joinpath('demo', 'demo-msbyte-lsbit-p4-u2.pcf'))
    font_4 = PcfFont.load(assets_dir.joinpath('demo', 'demo-msbyte-msbit-p4-u2.pcf'))
    font_5 = PcfFont.load(assets_dir.joinpath('demo', 'demo-lsbyte-lsbit-p2-u4.pcf'))
    font_6 = PcfFont.load(assets_dir.joinpath('demo', 'demo-lsbyte-msbit-p2-u4.pcf'))
    font_7 = PcfFont.load(assets_dir.joinpath('demo', 'demo-msbyte-lsbit-p2-u4.pcf'))
    font_8 = PcfFont.load(assets_dir.joinpath('demo', 'demo-msbyte-msbit-p2-u4.pcf'))

    for glyph_index, glyph in enumerate(font_0.glyphs):
        glyph_name_1 = font_1.glyph_names[glyph_index]
        glyph_name_2 = font_2.glyph_names[glyph_index]
        glyph_name_3 = font_3.glyph_names[glyph_index]
        glyph_name_4 = font_4.glyph_names[glyph_index]
        glyph_name_5 = font_5.glyph_names[glyph_index]
        glyph_name_6 = font_6.glyph_names[glyph_index]
        glyph_name_7 = font_7.glyph_names[glyph_index]
        glyph_name_8 = font_8.glyph_names[glyph_index]
        assert glyph.name == glyph_name_1 == glyph_name_2 == glyph_name_3 == glyph_name_4 == glyph_name_5 == glyph_name_6 == glyph_name_7 == glyph_name_8

        metric_1 = font_1.metrics[glyph_index]
        metric_2 = font_2.metrics[glyph_index]
        metric_3 = font_3.metrics[glyph_index]
        metric_4 = font_4.metrics[glyph_index]
        metric_5 = font_5.metrics[glyph_index]
        metric_6 = font_6.metrics[glyph_index]
        metric_7 = font_7.metrics[glyph_index]
        metric_8 = font_8.metrics[glyph_index]
        assert metric_1 == metric_2 == metric_3 == metric_4 == metric_5 == metric_6 == metric_7 == metric_8
        assert glyph.device_width_x == metric_1.character_width == metric_2.character_width == metric_3.character_width == metric_4.character_width == metric_5.character_width == metric_6.character_width == metric_7.character_width == metric_8.character_width
        assert glyph.dimensions == metric_1.dimensions == metric_2.dimensions == metric_3.dimensions == metric_4.dimensions == metric_5.dimensions == metric_6.dimensions == metric_7.dimensions == metric_8.dimensions
        assert glyph.offset == metric_1.offset == metric_2.offset == metric_3.offset == metric_4.offset == metric_5.offset == metric_6.offset == metric_7.offset == metric_8.offset

        bitmap_1 = font_1.bitmaps[glyph_index]
        bitmap_2 = font_2.bitmaps[glyph_index]
        bitmap_3 = font_3.bitmaps[glyph_index]
        bitmap_4 = font_4.bitmaps[glyph_index]
        bitmap_5 = font_5.bitmaps[glyph_index]
        bitmap_6 = font_6.bitmaps[glyph_index]
        bitmap_7 = font_7.bitmaps[glyph_index]
        bitmap_8 = font_8.bitmaps[glyph_index]
        assert glyph.bitmap == bitmap_1 == bitmap_2 == bitmap_3 == bitmap_4 == bitmap_5 == bitmap_6 == bitmap_7 == bitmap_8


def test_unifont(assets_dir: Path):
    font_1 = BdfFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.02.bdf'))
    font_2 = PcfFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.02.pcf'))

    for glyph_index, glyph in enumerate(font_1.glyphs):
        glyph_name = font_2.glyph_names[glyph_index]
        assert glyph.name == glyph_name

        metric = font_2.metrics[glyph_index]
        assert glyph.device_width_x == metric.character_width
        assert glyph.dimensions == metric.dimensions
        assert glyph.offset == metric.offset

        bitmap = font_2.bitmaps[glyph_index]
        assert glyph.bitmap == bitmap
