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
        print(f'offset: ({metric.left_side_bearing}, {-metric.descent})')
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
