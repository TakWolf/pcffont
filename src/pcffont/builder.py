import os

from pcffont.font import PcfFont
from pcffont.format import PcfTableFormat
from pcffont.glyph import PcfGlyph
from pcffont.t_properties import PcfProperties
from pcffont.t_accelerators import PcfAccelerators
from pcffont.t_metrics import PcfMetrics
from pcffont.t_bitmaps import PcfBitmaps
from pcffont.t_encodings import PcfBdfEncodings
from pcffont.t_scalable_widths import PcfScalableWidths
from pcffont.t_glyph_names import PcfGlyphNames


class PcfFontConfig:
    def __init__(
            self,
            font_ascent: int = 0,
            font_descent: int = 0,
            default_char: int = PcfBdfEncodings.NO_GLYPH_INDEX,
            draw_right_to_left: bool = False,
            ms_byte_first: bool = True,
            ms_bit_first: bool = True,
            glyph_pad_index: int = 0,
            scan_unit_index: int = 0,
    ):
        self.font_ascent = font_ascent
        self.font_descent = font_descent
        self.default_char = default_char
        self.draw_right_to_left = draw_right_to_left
        self.ms_byte_first = ms_byte_first
        self.ms_bit_first = ms_bit_first
        self.glyph_pad_index = glyph_pad_index
        self.scan_unit_index = scan_unit_index

    def to_table_format(self) -> PcfTableFormat:
        return PcfTableFormat(
            ms_byte_first=self.ms_byte_first,
            ms_bit_first=self.ms_bit_first,
            glyph_pad_index=self.glyph_pad_index,
            scan_unit_index=self.scan_unit_index,
        )


class PcfFontBuilder:
    def __init__(
            self,
            properties: PcfProperties = None,
            glyphs: list[PcfGlyph] = None,
            config: PcfFontConfig = None,
    ):
        if properties is None:
            properties = PcfProperties()
        self.properties = properties
        if glyphs is None:
            glyphs = list[PcfGlyph]()
        self.glyphs = glyphs
        if config is None:
            config = PcfFontConfig()
        self.config = config

    def build(self) -> PcfFont:
        bdf_encodings = PcfBdfEncodings(
            self.config.to_table_format(),
            default_char=self.config.default_char,
        )
        glyph_names = PcfGlyphNames(self.config.to_table_format())
        scalable_widths = PcfScalableWidths(self.config.to_table_format())
        metrics = PcfMetrics(self.config.to_table_format())
        bitmaps = PcfBitmaps(self.config.to_table_format())
        accelerators = PcfAccelerators(
            self.config.to_table_format(),
            draw_right_to_left=self.config.draw_right_to_left,
            font_ascent=self.config.font_ascent,
            font_descent=self.config.font_descent,
        )

        for glyph_index, glyph in enumerate(self.glyphs):
            if 0 <= glyph.encoding <= PcfBdfEncodings.MAX_ENCODING:
                bdf_encodings[glyph.encoding] = glyph_index
            glyph_names.append(glyph.name)
            scalable_widths.append(glyph.scalable_width)
            metrics.append(glyph.create_metric(False))
            bitmaps.append(glyph.bitmap)

        accelerators.min_bounds = metrics.calculate_min_bounds()
        accelerators.max_bounds = metrics.calculate_max_bounds()
        accelerators.max_overlap = metrics.calculate_max_overlap()
        accelerators.no_overlap = accelerators.max_overlap <= accelerators.min_bounds.left_side_bearing
        accelerators.constant_width = accelerators.min_bounds.character_width == accelerators.max_bounds.character_width
        accelerators.ink_inside = (accelerators.max_overlap <= 0 <= accelerators.min_bounds.left_side_bearing and
                                   accelerators.min_bounds.ascent >= -accelerators.font_descent and
                                   accelerators.max_bounds.ascent <= accelerators.font_ascent and
                                   -accelerators.min_bounds.descent <= accelerators.font_ascent and
                                   accelerators.max_bounds.descent <= accelerators.font_descent)

        if accelerators.min_bounds == accelerators.max_bounds:
            accelerators.constant_metrics = True
            accelerators.terminal_font = (accelerators.min_bounds.left_side_bearing == 0 and
                                          accelerators.min_bounds.right_side_bearing == accelerators.min_bounds.character_width and
                                          accelerators.min_bounds.ascent == accelerators.font_ascent and
                                          accelerators.min_bounds.descent == accelerators.font_descent)
        else:
            accelerators.constant_metrics = False
            accelerators.terminal_font = False

        if accelerators.constant_metrics:
            ink_metrics = PcfMetrics(self.config.to_table_format(), [glyph.create_metric(True) for glyph in self.glyphs])

            accelerators.ink_min_bounds = ink_metrics.calculate_min_bounds()
            accelerators.ink_max_bounds = ink_metrics.calculate_max_bounds()
            accelerators.table_format.ink_or_compressed_metrics = True
            accelerators.ink_metrics = True
        else:
            ink_metrics = None

            accelerators.table_format.ink_or_compressed_metrics = False
            accelerators.ink_metrics = False

        metrics.table_format.ink_or_compressed_metrics = metrics.calculate_compressible()
        if ink_metrics is not None:
            ink_metrics.table_format.ink_or_compressed_metrics = ink_metrics.calculate_compressible()

        font = PcfFont()
        font.bdf_encodings = bdf_encodings
        font.glyph_names = glyph_names
        font.scalable_widths = scalable_widths
        font.metrics = metrics
        font.ink_metrics = ink_metrics
        font.bitmaps = bitmaps
        font.accelerators = accelerators
        font.bdf_accelerators = accelerators
        font.properties = self.properties
        return font

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        self.build().save(file_path)
