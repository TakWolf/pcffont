# PcfFont

[![Python](https://img.shields.io/badge/python-3.10-brightgreen)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/pcffont)](https://pypi.org/project/pcffont/)

PcfFont is a library for manipulating [Portable Compiled Format (PCF) Fonts](https://en.wikipedia.org/wiki/Portable_Compiled_Format).

## Installation

```shell
pip install pcffont
```

## Usage

### Load

```python
import os
import shutil

from examples import assets_dir, build_dir
from pcffont import PcfFont


def main():
    outputs_dir = os.path.join(build_dir, 'load')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = PcfFont.load(os.path.join(assets_dir, 'unifont', 'unifont-15.1.05.pcf'))
    print(f'name: {font.properties.font}')
    print(f'size: {font.properties.pixel_size}')
    print(f'ascent: {font.accelerators.font_ascent}')
    print(f'descent: {font.accelerators.font_descent}')
    print()
    for code_point, glyph_index in sorted(font.bdf_encodings.items()):
        glyph_name = font.glyph_names[glyph_index]
        metric = font.metrics[glyph_index]
        bitmap = font.bitmaps[glyph_index]
        print(f'char: {chr(code_point)} ({code_point:04X})')
        print(f'glyph_name: {glyph_name}')
        print(f'advance_width: {metric.character_width}')
        print(f'dimensions: {metric.dimensions}')
        print(f'origin: {metric.origin}')
        for bitmap_row in bitmap:
            text = ''.join(map(str, bitmap_row)).replace('0', '  ').replace('1', '██')
            print(f'{text}*')
        print()
    font.save(os.path.join(outputs_dir, 'unifont-15.1.05.pcf'))


if __name__ == '__main__':
    main()
```

### Create

```python
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
    font.accelerators = PcfAccelerators(PcfTableFormat(has_ink_bounds=True))
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

Under the [MIT license](LICENSE).
