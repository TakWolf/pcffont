from enum import StrEnum


class WeightName(StrEnum):
    THIN = 'Thin'
    MEDIUM = 'Medium'
    BOLD = 'Bold'


class Slant(StrEnum):
    # Upright design
    ROMAN = 'R'
    # Italic design, slanted clockwise from the vertical
    ITALIC = 'I'
    # Obliqued upright design, slanted clockwise from the vertical
    OBLIQUE = 'O'
    # Italic design, slanted counterclockwise from the vertical
    REVERSE_ITALIC = 'RI'
    # Obliqued upright design, slanted counterclockwise from the vertical
    REVERSE_OBLIQUE = 'RO'
    # Other
    OTHER = 'OT'


class SetwidthName(StrEnum):
    NORMAL = 'Normal'
    CONDENSED = 'Condensed'
    NARROW = 'Narrow'
    DOUBLE_WIDE = 'Double Wide'


class AddStyleName(StrEnum):
    SERIF = 'Serif'
    SANS_SERIF = 'Sans Serif'
    INFORMAL = 'Informal'
    DECORATED = 'Decorated'


class Spacing(StrEnum):
    # Fixed pitch
    MONOSPACED = 'M'
    # Variable pitch
    PROPORTIONAL = 'P'
    # A special monospaced font that conforms to the traditional data-processing character cell font model
    CHAR_CELL = 'C'


class CharsetRegistry(StrEnum):
    ISO8859 = 'ISO8859'
    ISO10646 = 'ISO10646'
