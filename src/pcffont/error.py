
class PcfError(Exception):
    pass


class PcfPropKeyError(PcfError):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        super().__init__(f"'{key}': {reason}")


class PcfPropValueError(PcfError):
    def __init__(self, key: str, value: object, reason: str):
        self.key = key
        self.value = value
        self.reason = reason
        super().__init__(f"'{key}': '{value}': {reason}")


class PcfXlfdError(PcfError):
    def __init__(self, font_name: str, reason: str):
        self.font_name = font_name
        self.reason = reason
        super().__init__(f"'{font_name}': {reason}")
