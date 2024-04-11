import hashlib
import io
import os

from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _test_dump(file_name: str):
    file_path = os.path.join(project_root_dir, 'assets', file_name)
    with open(file_path, 'rb') as file:
        buffer_in = Buffer(file)
        buffer_out = Buffer(io.BytesIO())

        headers = PcfHeader.parse(buffer_in)
        PcfHeader.dump(buffer_out, headers)
        buffer_in.seek(0)
        buffer_out.seek(0)
        headers_data_size = 4 + 4 + (4 * 4) * len(headers)
        headers_data_in = buffer_in.read(headers_data_size)
        headers_data_out = buffer_out.read(headers_data_size)
        assert _sha256(headers_data_in) == _sha256(headers_data_out)

        for header in headers:
            table = util.parse_table(buffer_in, header)
            if table is None:
                continue
            table_offset = header.table_offset
            table_size = table.dump(buffer_out, table_offset, compat_mode=True)
            assert table_size == header.table_size
            buffer_in.seek(table_offset)
            buffer_out.seek(table_offset)
            table_data_in = buffer_in.read(table_size)
            table_data_out = buffer_out.read(table_size)
            assert _sha256(table_data_in) == _sha256(table_data_out)


def test_unifont():
    _test_dump('unifont/unifont-15.1.05.pcf')


def test_dweep():
    _test_dump('dweep/dweep.pcf')


def test_rock36():
    _test_dump('sgi/rock36.pcf')


def test_raize():
    _test_dump('raize/raize-normal-19.pcf')


def test_anorexia():
    _test_dump('artwiz/anorexia.pcf')


def test_kates():
    _test_dump('artwiz/kates.pcf')


def test_trisk():
    _test_dump('trisk/trisk.pcf')


def test_profont():
    _test_dump('profont-x11/ProFont_r400-29.pcf')
