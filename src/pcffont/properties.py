import re
from collections import UserDict

from pcffont.error import PcfError, PcfPropKeyError, PcfPropValueError, PcfXlfdError
from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.stream import Buffer
from pcffont.table import PcfTable

_KEY_FOUNDRY = 'FOUNDRY'
_KEY_FAMILY_NAME = 'FAMILY_NAME'
_KEY_WEIGHT_NAME = 'WEIGHT_NAME'
_KEY_SLANT = 'SLANT'
_KEY_SETWIDTH_NAME = 'SETWIDTH_NAME'
_KEY_ADD_STYLE_NAME = 'ADD_STYLE_NAME'
_KEY_PIXEL_SIZE = 'PIXEL_SIZE'
_KEY_POINT_SIZE = 'POINT_SIZE'
_KEY_RESOLUTION_X = 'RESOLUTION_X'
_KEY_RESOLUTION_Y = 'RESOLUTION_Y'
_KEY_SPACING = 'SPACING'
_KEY_AVERAGE_WIDTH = 'AVERAGE_WIDTH'
_KEY_CHARSET_REGISTRY = 'CHARSET_REGISTRY'
_KEY_CHARSET_ENCODING = 'CHARSET_ENCODING'

_KEY_CAP_HEIGHT = 'CAP_HEIGHT'
_KEY_X_HEIGHT = 'X_HEIGHT'

_KEY_FONT = 'FONT'
_KEY_FONT_VERSION = 'FONT_VERSION'
_KEY_COPYRIGHT = 'COPYRIGHT'
_KEY_NOTICE = 'NOTICE'

_STR_VALUE_KEYS = {
    _KEY_FOUNDRY,
    _KEY_FAMILY_NAME,
    _KEY_WEIGHT_NAME,
    _KEY_SLANT,
    _KEY_SETWIDTH_NAME,
    _KEY_ADD_STYLE_NAME,
    _KEY_SPACING,
    _KEY_CHARSET_REGISTRY,
    _KEY_CHARSET_ENCODING,
    _KEY_FONT,
    _KEY_FONT_VERSION,
    _KEY_COPYRIGHT,
    _KEY_NOTICE,
}

_INT_VALUE_KEYS = {
    _KEY_PIXEL_SIZE,
    _KEY_POINT_SIZE,
    _KEY_RESOLUTION_X,
    _KEY_RESOLUTION_Y,
    _KEY_AVERAGE_WIDTH,
    _KEY_CAP_HEIGHT,
    _KEY_X_HEIGHT,
}

_XLFD_FONT_NAME_STR_VALUE_KEYS = {
    _KEY_FOUNDRY,
    _KEY_FAMILY_NAME,
    _KEY_WEIGHT_NAME,
    _KEY_SLANT,
    _KEY_SETWIDTH_NAME,
    _KEY_ADD_STYLE_NAME,
    _KEY_SPACING,
    _KEY_CHARSET_REGISTRY,
    _KEY_CHARSET_ENCODING,
}

_XLFD_FONT_NAME_KEYS_ORDER = [
    _KEY_FOUNDRY,
    _KEY_FAMILY_NAME,
    _KEY_WEIGHT_NAME,
    _KEY_SLANT,
    _KEY_SETWIDTH_NAME,
    _KEY_ADD_STYLE_NAME,
    _KEY_PIXEL_SIZE,
    _KEY_POINT_SIZE,
    _KEY_RESOLUTION_X,
    _KEY_RESOLUTION_Y,
    _KEY_SPACING,
    _KEY_AVERAGE_WIDTH,
    _KEY_CHARSET_REGISTRY,
    _KEY_CHARSET_ENCODING,
]


def _check_key(key: str):
    if not key.replace('_', '').isalnum():
        raise PcfPropKeyError(key, 'contains illegal characters')


def _check_value(key: str, value: str | int):
    if key in _STR_VALUE_KEYS:
        if not isinstance(value, str):
            raise PcfPropValueError(key, value, f"expected type 'str', got '{type(value).__name__}' instead")
    elif key in _INT_VALUE_KEYS:
        if not isinstance(value, int):
            raise PcfPropValueError(key, value, f"expected type 'int', got '{type(value).__name__}' instead")
    else:
        if not isinstance(value, str) and not isinstance(value, int):
            raise PcfPropValueError(key, value, f"expected type 'str | int', got '{type(value).__name__}' instead")
    if key in _XLFD_FONT_NAME_STR_VALUE_KEYS:
        matched = re.search(r'[-?*,"]', value)
        if matched is not None:
            raise PcfPropValueError(key, value, f"contains illegal characters '{matched.group()}'")


class PcfProperties(PcfTable, UserDict[str, str | int | None]):
    @staticmethod
    def parse(buffer: Buffer, header: PcfHeader) -> 'PcfProperties':
        _, byte_order = header.get_and_check_table_format(buffer)

        props_count = buffer.read_int(byte_order)

        prop_infos = []
        for _ in range(props_count):
            key_offset = buffer.read_int(byte_order)
            is_string_prop = buffer.read_bool()
            value = buffer.read_int(byte_order)
            prop_infos.append((key_offset, is_string_prop, value))

        # Pad to next int32 boundary
        if (props_count & 3) != 0:
            buffer.skip(4 - (props_count & 3))

        buffer.skip_int()  # strings_size
        strings_start = buffer.tell()

        data = {}
        for key_offset, is_string_prop, value in prop_infos:
            buffer.seek(strings_start + key_offset)
            key = buffer.read_string()
            if is_string_prop:
                buffer.seek(strings_start + value)
                value = buffer.read_string()
            else:
                value = int(value)
            data[key] = value

        return PcfProperties(data)

    def __init__(self, data: dict[str, str | int | None] = None):
        super().__init__(data)

    def __getitem__(self, key: str) -> str | int:
        key = key.upper()
        _check_key(key)
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: str | int | None):
        key = key.upper()
        _check_key(key)
        if value is None:
            self.pop(key, None)
        else:
            _check_value(key, value)
            super().__setitem__(key, value)

    @property
    def table_type(self) -> PcfTableType:
        return PcfTableType.PROPERTIES

    @property
    def foundry(self) -> str | None:
        return self.get(_KEY_FOUNDRY, None)

    @foundry.setter
    def foundry(self, value: str | None):
        self[_KEY_FOUNDRY] = value

    @property
    def family_name(self) -> str | None:
        return self.get(_KEY_FAMILY_NAME, None)

    @family_name.setter
    def family_name(self, value: str | None):
        self[_KEY_FAMILY_NAME] = value

    @property
    def weight_name(self) -> str | None:
        return self.get(_KEY_WEIGHT_NAME, None)

    @weight_name.setter
    def weight_name(self, value: str | None):
        self[_KEY_WEIGHT_NAME] = value

    @property
    def slant(self) -> str | None:
        return self.get(_KEY_SLANT, None)

    @slant.setter
    def slant(self, value: str | None):
        self[_KEY_SLANT] = value

    @property
    def setwidth_name(self) -> str | None:
        return self.get(_KEY_SETWIDTH_NAME, None)

    @setwidth_name.setter
    def setwidth_name(self, value: str | None):
        self[_KEY_SETWIDTH_NAME] = value

    @property
    def add_style_name(self) -> str | None:
        return self.get(_KEY_ADD_STYLE_NAME, None)

    @add_style_name.setter
    def add_style_name(self, value: str | None):
        self[_KEY_ADD_STYLE_NAME] = value

    @property
    def pixel_size(self) -> int | None:
        return self.get(_KEY_PIXEL_SIZE, None)

    @pixel_size.setter
    def pixel_size(self, value: int | None):
        self[_KEY_PIXEL_SIZE] = value

    @property
    def point_size(self) -> int | None:
        return self.get(_KEY_POINT_SIZE, None)

    @point_size.setter
    def point_size(self, value: int | None):
        self[_KEY_POINT_SIZE] = value

    @property
    def resolution_x(self) -> int | None:
        return self.get(_KEY_RESOLUTION_X, None)

    @resolution_x.setter
    def resolution_x(self, value: int | None):
        self[_KEY_RESOLUTION_X] = value

    @property
    def resolution_y(self) -> int | None:
        return self.get(_KEY_RESOLUTION_Y, None)

    @resolution_y.setter
    def resolution_y(self, value: int | None):
        self[_KEY_RESOLUTION_Y] = value

    @property
    def spacing(self) -> str | None:
        return self.get(_KEY_SPACING, None)

    @spacing.setter
    def spacing(self, value: str | None):
        self[_KEY_SPACING] = value

    @property
    def average_width(self) -> int | None:
        return self.get(_KEY_AVERAGE_WIDTH, None)

    @average_width.setter
    def average_width(self, value: int | None):
        self[_KEY_AVERAGE_WIDTH] = value

    @property
    def charset_registry(self) -> str | None:
        return self.get(_KEY_CHARSET_REGISTRY, None)

    @charset_registry.setter
    def charset_registry(self, value: str | None):
        self[_KEY_CHARSET_REGISTRY] = value

    @property
    def charset_encoding(self) -> str | None:
        return self.get(_KEY_CHARSET_ENCODING, None)

    @charset_encoding.setter
    def charset_encoding(self, value: str | None):
        self[_KEY_CHARSET_ENCODING] = value

    @property
    def x_height(self) -> int | None:
        return self.get(_KEY_X_HEIGHT, None)

    @x_height.setter
    def x_height(self, value: int | None):
        self[_KEY_X_HEIGHT] = value

    @property
    def cap_height(self) -> int | None:
        return self.get(_KEY_CAP_HEIGHT, None)

    @cap_height.setter
    def cap_height(self, value: int | None):
        self[_KEY_CAP_HEIGHT] = value

    @property
    def font(self) -> str | None:
        return self.get(_KEY_FONT, None)

    @font.setter
    def font(self, value: str | None):
        self[_KEY_FONT] = value

    @property
    def font_version(self) -> str | None:
        return self.get(_KEY_FONT_VERSION, None)

    @font_version.setter
    def font_version(self, value: str | None):
        self[_KEY_FONT_VERSION] = value

    @property
    def copyright(self) -> str | None:
        return self.get(_KEY_COPYRIGHT, None)

    @copyright.setter
    def copyright(self, value: str | None):
        self[_KEY_COPYRIGHT] = value

    @property
    def notice(self) -> str | None:
        return self.get(_KEY_NOTICE, None)

    @notice.setter
    def notice(self, value: str | None):
        self[_KEY_NOTICE] = value

    def generate_xlfd(self):
        tokens = ['']
        for key in _XLFD_FONT_NAME_KEYS_ORDER:
            tokens.append(str(self.get(key, '')))
        self.font = '-'.join(tokens)

    def update_by_xlfd(self):
        if self.font is None:
            raise PcfError(f"'{_KEY_FONT}' not set")
        if not self.font.startswith('-'):
            raise PcfXlfdError(self.font, "not starts with '-'")
        if self.font.count('-') != 14:
            raise PcfXlfdError(self.font, "there could only be 14 '-' in the name")
        tokens = self.font.removeprefix('-').split('-')
        for index, token in enumerate(tokens):
            key = _XLFD_FONT_NAME_KEYS_ORDER[index]
            if token == '':
                value = None
            else:
                if key in _XLFD_FONT_NAME_STR_VALUE_KEYS:
                    value = token
                else:
                    value = int(token)
            self[key] = value

    def dump(self, buffer: Buffer, table_offset: int) -> tuple[int, int]:
        table_format = 0b1110
        props_count = len(self)

        # Pad to next int32 boundary
        padding = 0
        if (props_count & 3) != 0:
            padding = 4 - (props_count & 3)

        strings_start = table_offset + 4 + 4 + (4 + 1 + 4) * props_count + padding + 4
        strings_size = 0
        prop_infos = []
        buffer.seek(strings_start)
        for key, value in self.items():
            key_offset = strings_size
            strings_size += buffer.write_string(key)
            value_offset = strings_size
            if isinstance(value, str):
                strings_size += buffer.write_string(value)
            prop_infos.append((key, key_offset, value, value_offset))

        padding2 = 4 - strings_size % 4
        table_size = strings_start - table_offset + strings_size + padding2

        buffer.seek(table_offset)
        buffer.write_int_le(table_format)
        buffer.write_int_be(props_count)
        for key, key_offset, value, value_offset in prop_infos:
            buffer.write_int_be(key_offset)
            if isinstance(value, str):
                buffer.write_bool(True)
                buffer.write_int_be(value_offset)
            else:
                buffer.write_bool(False)
                buffer.write_int_be(value)
        buffer.write_nulls(padding)
        buffer.write_int_be(strings_size)
        buffer.skip(strings_size)
        buffer.write_nulls(padding2)

        return table_format, table_size
