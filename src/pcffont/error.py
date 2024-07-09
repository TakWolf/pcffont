from typing import Any


class PcfError(Exception):
    pass


class PcfParseError(PcfError):
    pass


class PcfPropKeyError(PcfError):
    key: Any
    reason: str

    def __init__(self, key: Any, reason: str):
        self.key = key
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.reason}: key = {repr(self.key)}'


class PcfPropValueError(PcfError):
    key: str
    value: Any
    reason: str

    def __init__(self, key: str, value: Any, reason: str):
        self.key = key
        self.value = value
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.reason}: key = {repr(self.key)}, value = {repr(self.value)}'


class PcfXlfdError(PcfError):
    font_name: str
    reason: str

    def __init__(self, font_name: str, reason: str):
        self.font_name = font_name
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.reason}: {self.font_name}'


class PcfOutOfRangeError(PcfError):
    pass
