
class PcfError(Exception):
    pass


class PcfParseError(PcfError):
    pass


class PcfXlfdError(PcfError):
    pass


class PcfOutOfRangeError(PcfError):
    pass
