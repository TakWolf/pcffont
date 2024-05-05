import os
import shutil

from examples import build_dir
from pcffont import PcfFont, PcfTableFormat, PcfMetric, PcfProperties, PcfAccelerators, PcfMetrics, PcfBitmaps, PcfBdfEncodings, PcfScalableWidths, PcfGlyphNames


def main():
    outputs_dir = os.path.join(build_dir, 'create')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = PcfFont()
    font.bdf_encodings = PcfBdfEncodings()
    font.glyph_names = PcfGlyphNames()
    font.metrics = PcfMetrics()
    font.ink_metrics = PcfMetrics()
    font.scalable_widths = PcfScalableWidths()
    font.bitmaps = PcfBitmaps()
    font.accelerators = PcfAccelerators(PcfTableFormat(ink_metrics=True))
    font.bdf_accelerators = font.accelerators
    font.properties = PcfProperties()

    font.bdf_encodings[ord('A')] = len(font.glyph_names)
    font.glyph_names.append('A')
    font.metrics.append(PcfMetric(
        left_side_bearing=0,
        right_side_bearing=8,
        character_width=8,
        ascent=14,
        descent=2,
    ))
    font.ink_metrics.append(PcfMetric(
        left_side_bearing=1,
        right_side_bearing=7,
        character_width=8,
        ascent=10,
        descent=0,
    ))
    font.scalable_widths.append(500)
    font.bitmaps.append([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    font.accelerators.no_overlap = True
    font.accelerators.ink_inside = True
    font.accelerators.ink_metrics = True
    font.accelerators.font_ascent = 14
    font.accelerators.font_descent = 2
    font.accelerators.min_bounds = font.metrics[0]
    font.accelerators.max_bounds = font.metrics[0]
    font.accelerators.ink_min_bounds = font.ink_metrics[0]
    font.accelerators.ink_max_bounds = font.ink_metrics[0]

    font.properties.foundry = 'Pixel Font Studio'
    font.properties.family_name = 'Demo Pixel'
    font.properties.weight_name = 'Medium'
    font.properties.slant = 'R'
    font.properties.setwidth_name = 'Normal'
    font.properties.add_style_name = 'Sans Serif'
    font.properties.pixel_size = 16
    font.properties.point_size = font.properties.pixel_size * 10
    font.properties.resolution_x = 75
    font.properties.resolution_y = 75
    font.properties.spacing = 'P'
    font.properties.average_width = round(sum([metric.character_width * 10 for metric in font.metrics]) / len(font.metrics))
    font.properties.charset_registry = 'ISO10646'
    font.properties.charset_encoding = '1'
    font.properties.generate_xlfd()

    font.properties.x_height = 5
    font.properties.cap_height = 7

    font.properties.font_version = '1.0.0'
    font.properties.copyright = 'Copyright (c) TakWolf'

    font.save(os.path.join(outputs_dir, 'my-font.pcf'))


if __name__ == '__main__':
    main()
