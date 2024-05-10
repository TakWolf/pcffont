import os
import shutil

from examples import build_dir
from pcffont import PcfFontBuilder, PcfGlyph


def main():
    outputs_dir = os.path.join(build_dir, 'create')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    builder = PcfFontBuilder()
    builder.config.font_ascent = 14
    builder.config.font_descent = 2

    builder.glyphs.append(PcfGlyph(
        name='A',
        encoding=ord('A'),
        scalable_width=500,
        character_width=8,
        dimensions=(8, 16),
        origin=(0, -2),
        bitmap=[
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
        ],
    ))

    builder.properties.foundry = 'Pixel Font Studio'
    builder.properties.family_name = 'Demo Pixel'
    builder.properties.weight_name = 'Medium'
    builder.properties.slant = 'R'
    builder.properties.setwidth_name = 'Normal'
    builder.properties.add_style_name = 'Sans Serif'
    builder.properties.pixel_size = 16
    builder.properties.point_size = builder.properties.pixel_size * 10
    builder.properties.resolution_x = 75
    builder.properties.resolution_y = 75
    builder.properties.spacing = 'P'
    builder.properties.average_width = round(sum([glyph.character_width * 10 for glyph in builder.glyphs]) / len(builder.glyphs))
    builder.properties.charset_registry = 'ISO10646'
    builder.properties.charset_encoding = '1'
    builder.properties.generate_xlfd()

    builder.properties.x_height = 5
    builder.properties.cap_height = 7

    builder.properties.font_version = '1.0.0'
    builder.properties.copyright = 'Copyright (c) TakWolf'

    builder.save(os.path.join(outputs_dir, 'my-font.pcf'))


if __name__ == '__main__':
    main()
