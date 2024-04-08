from collections import UserDict

from pcffont.internal.stream import ByteOrder, Buffer


class PcfProperties(UserDict[str, str | int | None]):
    @staticmethod
    def parse(buffer: Buffer, byte_order: ByteOrder) -> 'PcfProperties':
        props_count = buffer.read_int(byte_order)

        prop_infos = []
        for _ in range(props_count):
            key_offset = buffer.read_int(byte_order)
            is_string_prop = buffer.read_byte() != b'\x00'
            value = buffer.read_int(byte_order)
            prop_infos.append((key_offset, is_string_prop, value))

        if (props_count & 3) != 0:
            # Pad to next int32 boundary
            buffer.skip(4 - (props_count & 3))

        buffer.skip_int()  # strings_size
        strings_start = buffer.tell()

        data = {}
        for key_offset, is_string_prop, value in prop_infos:
            buffer.seek(strings_start + key_offset)
            key = buffer.read_until(b'\x00').decode('utf-8')
            if is_string_prop:
                buffer.seek(strings_start + value)
                value = buffer.read_until(b'\x00').decode('utf-8')
            else:
                value = int(value)
            data[key] = value
        return PcfProperties(data)

    def __init__(self, data: dict[str, str | int | None] = None):
        super().__init__(data)

    def __getitem__(self, key: str) -> str | int:
        key = key.upper()
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: str | int | None):
        key = key.upper()
        if value is None:
            self.pop(key, None)
        else:
            super().__setitem__(key, value)
