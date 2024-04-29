
class PcfError(Exception):
    pass


class PcfParseError(PcfError):
    pass


class PcfTableTypeError(PcfError):
    pass


class PcfPropKeyError(PcfError):
    def __init__(self, key: str, reason: str):
        super().__init__(f"'{key}': {reason}")
        self.key = key
        self.reason = reason


class PcfPropValueError(PcfError):
    def __init__(self, key: str, value: object, reason: str):
        super().__init__(f"'{key}': '{value}': {reason}")
        self.key = key
        self.value = value
        self.reason = reason


class PcfXlfdError(PcfError):
    def __init__(self, font_name: str, reason: str):
        super().__init__(f"'{font_name}': {reason}")
        self.font_name = font_name
        self.reason = reason


class PcfOutOfRangeError(PcfError):
    pass
