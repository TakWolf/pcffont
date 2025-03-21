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
