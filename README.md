# PcfFont.Python

[![Python](https://img.shields.io/badge/python-3.10-brightgreen)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/pcffont)](https://pypi.org/project/pcffont/)

PcfFont is a library for manipulating [Portable Compiled Format (PCF) Fonts](https://en.wikipedia.org/wiki/Portable_Compiled_Format).

## Installation

```shell
pip install pcffont
```

## Usage

### Create

```python
import shutil

from examples import build_dir
from pcffont import PcfFontBuilder, PcfGlyph


def main():
    outputs_dir = build_dir.joinpath('create')
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir(parents=True)

    builder = PcfFontBuilder()
    builder.config.font_ascent = 14
    builder.config.font_descent = 2

    builder.glyphs.append(PcfGlyph(
        name='A',
        encoding=65,
        scalable_width=500,
        character_width=8,
        dimensions=(8, 16),
        offset=(0, -2),
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
    builder.properties.family_name = 'My Font'
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

    builder.properties.x_height = 7
    builder.properties.cap_height = 10

    builder.properties.font_version = '1.0.0'
    builder.properties.copyright = 'Copyright (c) TakWolf'

    builder.save(outputs_dir.joinpath('my-font.pcf'))


if __name__ == '__main__':
    main()
```

### Load

```python
import shutil

from examples import assets_dir, build_dir
from pcffont import PcfFont


def main():
    outputs_dir = build_dir.joinpath('load')
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir(parents=True)

    font = PcfFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.02.pcf'))
    print(f'name: {font.properties.font}')
    print(f'size: {font.properties.pixel_size}')
    print(f'ascent: {font.accelerators.font_ascent}')
    print(f'descent: {font.accelerators.font_descent}')
    print()
    for encoding, glyph_index in sorted(font.bdf_encodings.items()):
        glyph_name = font.glyph_names[glyph_index]
        metric = font.metrics[glyph_index]
        bitmap = font.bitmaps[glyph_index]
        print(f'char: {chr(encoding)} ({encoding:04X})')
        print(f'glyph_name: {glyph_name}')
        print(f'advance_width: {metric.character_width}')
        print(f'dimensions: {metric.dimensions}')
        print(f'offset: {metric.offset}')
        for bitmap_row in bitmap:
            text = ''.join('  ' if color == 0 else '██' for color in bitmap_row)
            print(f'{text}*')
        print()
    font.save(outputs_dir.joinpath('unifont-16.0.02.pcf'))


if __name__ == '__main__':
    main()
```

## Test Fonts

- [GNU Unifont Glyphs](https://unifoundry.com/unifont/index.html)
- [Spleen](https://github.com/fcambus/spleen)

## References

- [FreeType font driver for PCF fonts](https://github.com/freetype/freetype/tree/master/src/pcf)
- [FontForge - The X11 PCF bitmap font file format](https://fontforge.org/docs/techref/pcf-format.html)
- [The X Font Library](https://www.x.org/releases/current/doc/libXfont/fontlib.html)
- [bdftopcf](https://gitlab.freedesktop.org/xorg/util/bdftopcf)
- [bdftopcf - docs](https://www.x.org/releases/current/doc/man/man1/bdftopcf.1.xhtml)
- [X Logical Font Description Conventions - X Consortium Standard](https://www.x.org/releases/current/doc/xorg-docs/xlfd/xlfd.html)

## License

[MIT License](LICENSE)
