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

    encodings = PcfBdfEncodings()
    glyph_names = PcfGlyphNames()
    metrics = PcfMetrics()
    scalable_widths = PcfScalableWidths()
    bitmaps = PcfBitmaps()

    encodings[ord('A')] = len(glyph_names)
    glyph_names.append('A')
    metrics.append(PcfMetric(
        left_side_bearing=0,
        right_side_bearing=8,
        character_width=8,
        ascent=14,
        descent=2,
    ))
    scalable_widths.append(500)
    bitmaps.append([
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

    font.bdf_encodings = encodings
    font.glyph_names = glyph_names
    font.metrics = metrics
    font.ink_metrics = metrics
    font.scalable_widths = scalable_widths
    font.bitmaps = bitmaps

    accelerators = PcfAccelerators(PcfTableFormat(has_ink_bounds=True))
    accelerators.no_overlap = True
    accelerators.ink_inside = True
    accelerators.ink_metrics = True
    accelerators.font_ascent = 14
    accelerators.font_descent = 2
    accelerators.min_bounds = metrics[0]
    accelerators.max_bounds = metrics[0]
    accelerators.ink_min_bounds = metrics[0]
    accelerators.ink_max_bounds = metrics[0]
    font.accelerators = accelerators
    font.bdf_accelerators = accelerators

    properties = PcfProperties()
    properties.foundry = 'Pixel Font Studio'
    properties.family_name = 'Demo Pixel'
    properties.weight_name = 'Medium'
    properties.slant = 'R'
    properties.setwidth_name = 'Normal'
    properties.add_style_name = 'Sans Serif'
    properties.pixel_size = 16
    properties.point_size = properties.pixel_size * 10
    properties.resolution_x = 75
    properties.resolution_y = 75
    properties.spacing = 'P'
    properties.average_width = round(sum([metric.character_width * 10 for metric in font.metrics]) / len(font.metrics))
    properties.charset_registry = 'ISO10646'
    properties.charset_encoding = '1'
    properties.generate_xlfd()
    properties.x_height = 5
    properties.cap_height = 7
    properties.font_version = '1.0.0'
    properties.copyright = 'Copyright (c) TakWolf'
    font.properties = properties

    font.save(os.path.join(outputs_dir, 'my-font.pcf'))


if __name__ == '__main__':
    main()
